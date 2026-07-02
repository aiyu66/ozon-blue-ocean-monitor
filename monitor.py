"""
Ozon蓝海自动监控系统 — 主爬取脚本
使用 Playwright 定时爬取Ozon品类搜索页，提取竞争指标
输出JSON数据供分析引擎和Dashboard使用
"""

import json
import os
import sys
import time
import random
import re
from datetime import datetime, timedelta
from pathlib import Path

# 加载配置
from config import MONITOR_KEYWORDS, SCRAPER_CONFIG, DATA_CONFIG

# 项目根目录
PROJECT_ROOT = Path(__file__).parent


class OzonScraper:
    """Ozon搜索结果页爬取器"""

    def __init__(self, headless=True, use_stealth=True):
        self.headless = headless
        self.use_stealth = use_stealth
        self.browser = None
        self.context = None
        self.page = None

    async def init_browser(self):
        """初始化Playwright浏览器"""
        from playwright.async_api import async_playwright

        playwright = await async_playwright().start()

        # 启动浏览器
        ci_env = os.environ.get("CI", "").lower() == "true"
        launch_args = [
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
        if ci_env:
            # GitHub Actions环境需要额外参数
            launch_args.extend([
                "--disable-gpu",
                "--single-process",
                "--no-zygote",
            ])

        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=launch_args,
        )

        # 创建上下文（设置俄罗斯地区）
        self.context = await self.browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            locale="ru-RU",
            timezone_id="Europe/Moscow",
            geolocation={"latitude": 55.7558, "longitude": 37.6176},
            permissions=["geolocation"],
        )

        # stealth: 注入反检测脚本
        if self.use_stealth:
            await self.context.add_init_script("""
                // 隐藏 webdriver 标记
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                // 修改 plugins 长度
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                // 修改 languages
                Object.defineProperty(navigator, 'languages', {get: () => ['ru-RU', 'ru', 'en-US', 'en']});
                // 隐藏 automation 相关属性
                window.chrome = {runtime: {}};
            """)

        self.page = await self.context.new_page()
        print("✅ 浏览器初始化完成")

    async def close_browser(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
            print("✅ 浏览器已关闭")

    async def scrape_keyword(self, keyword_ru, keyword_en, max_pages=3):
        """
        爬取指定关键词在Ozon的搜索结果
        返回: {
            keyword, search_results_count, products: [...],
            avg_price, avg_reviews, seller_count, ozon_self_ratio,
            price_distribution, rating_distribution
        }
        """
        url = f"https://www.ozon.ru/search/?text={keyword_ru}&sorting=rating"
        print(f"\n🔍 正在爬取: {keyword_ru} ({keyword_en})")
        print(f"   URL: {url}")

        all_products = []
        total_results_count = 0

        try:
            # 第一页
            await self.page.goto(url, timeout=SCRAPER_CONFIG["timeout"] * 1000)
            await self.page.wait_for_load_state("networkidle")
            await self._random_delay(2, 4)

            # 获取搜索结果总数
            total_results_count = await self._get_total_results()

            # 爬取第一页商品数据
            page_products = await self._extract_products()
            all_products.extend(page_products)
            print(f"   第1页: 获取 {len(page_products)} 个商品, 总结果数: {total_results_count}")

            # 爬取后续页
            for page_num in range(2, max_pages + 1):
                # 点击下一页或修改URL
                next_url = f"{url}&page={page_num}"
                await self.page.goto(next_url, timeout=SCRAPER_CONFIG["timeout"] * 1000)
                await self.page.wait_for_load_state("networkidle")
                await self._random_delay(2, 4)

                page_products = await self._extract_products()
                if not page_products:
                    print(f"   第{page_num}页: 无商品数据，停止翻页")
                    break

                all_products.extend(page_products)
                print(f"   第{page_num}页: 获取 {len(page_products)} 个商品")

                # 关键词间延迟
                await self._random_delay(
                    SCRAPER_CONFIG["page_delay"],
                    SCRAPER_CONFIG["page_delay"] + 3
                )

        except Exception as e:
            print(f"   ❌ 爬取失败: {e}")

        # 计算汇总指标
        summary = self._calculate_summary(keyword_ru, keyword_en, total_results_count, all_products)
        return summary

    async def _get_total_results(self):
        """获取搜索结果总数"""
        try:
            # 尝试从页面元素获取总数
            count_el = await self.page.query_selector('[class*="search-results-count"], [class*="totalResults"], [data-widget="searchResultsV2"]')
            if count_el:
                text = await count_el.inner_text()
                match = re.search(r'(\d+[\s\d]*)', text)
                if match:
                    return int(match.group(1).replace(" ", ""))

            # fallback: 从搜索结果区域推算
            widgets = await self.page.query_selector_all('[data-widget="searchResultsV2"] [class*="item"], [data-widget="searchResultsV2"] a[class*="tile"]')
            return len(widgets) * 10  # 粗略估算

        except Exception:
            return 0

    async def _extract_products(self):
        """提取当前页面所有商品数据"""
        products = []

        try:
            # 等待商品列表加载
            await self.page.wait_for_selector('[data-widget="searchResultsV2"]', timeout=10000)

            # 找到所有商品卡片
            items = await self.page.query_selector_all(
                '[data-widget="searchResultsV2"] [class*="tile"]'
            )

            if not items:
                # 尝备选择器
                items = await self.page.query_selector_all(
                    '[data-widget="searchResultsV2"] a[href*="/product/"]'
                )

            for idx, item in enumerate(items[:SCRAPER_CONFIG["items_per_page"]]):
                try:
                    product = await self._extract_product_data(item, idx)
                    if product and product.get("price", 0) > 0:
                        products.append(product)
                except Exception:
                    continue

        except Exception as e:
            print(f"   提取商品数据异常: {e}")

        return products

    async def _extract_product_data(self, item, index):
        """提取单个商品的详细数据"""
        product = {}

        try:
            # 商品名称
            title_el = await item.query_selector('[class*="title"], [class*="name"], h3, h4, span[class*="ts"]')
            if title_el:
                product["title"] = await title_el.inner_text()
            else:
                product["title"] = ""

            # 价格
            price_el = await item.query_selector('[class*="price"], [data-widget="price"]')
            if price_el:
                price_text = await price_el.inner_text()
                # 提取数字（去除₽符号和空格）
                price_match = re.search(r'(\d+[\s\d]*)', price_text.replace(",", ""))
                if price_match:
                    product["price"] = int(price_match.group(1).replace(" ", ""))
                else:
                    product["price"] = 0
            else:
                product["price"] = 0

            # 折扣价
            discount_el = await item.query_selector('[class*="discount-price"], [class*="salePrice"]')
            if discount_el:
                discount_text = await discount_el.inner_text()
                discount_match = re.search(r'(\d+[\s\d]*)', discount_text.replace(",", ""))
                if discount_match:
                    product["discount_price"] = int(discount_match.group(1).replace(" ", ""))

            # 评分
            rating_el = await item.query_selector('[class*="rating"], [class*="stars"]')
            if rating_el:
                rating_text = await rating_el.inner_text()
                rating_match = re.search(r'(\d+[\.,]?\d*)', rating_text)
                if rating_match:
                    product["rating"] = float(rating_match.group(1).replace(",", "."))

            # 评论数
            review_el = await item.query_selector('[class*="review"], [class*="comment"], [class*="feedback"]')
            if review_el:
                review_text = await review_el.inner_text()
                review_match = re.search(r'(\d+)', review_text)
                if review_match:
                    product["reviews"] = int(review_match.group(1))
                else:
                    product["reviews"] = 0
            else:
                product["reviews"] = 0

            # 卖家信息（判断是否自营）
            seller_el = await item.query_selector('[class*="seller"], [class*="store"]')
            if seller_el:
                seller_text = await seller_el.inner_text()
                product["seller"] = seller_text
                product["is_ozon_self"] = "Ozon" in seller_text or "ozon" in seller_text.lower()
            else:
                product["seller"] = ""
                product["is_ozon_self"] = False

            # 商品链接
            link_el = await item.query_selector("a[href*='/product/']")
            if link_el:
                href = await link_el.get_attribute("href")
                product["url"] = f"https://www.ozon.ru{href}" if href and href.startswith("/") else href or ""
            else:
                product["url"] = ""

            product["position"] = index + 1

        except Exception:
            pass

        return product

    def _calculate_summary(self, keyword_ru, keyword_en, total_results, products):
        """根据爬取数据计算品类汇总指标"""
        if not products:
            return {
                "keyword_ru": keyword_ru,
                "keyword_en": keyword_en,
                "timestamp": datetime.now().isoformat(),
                "total_search_results": total_results,
                "scraped_products": 0,
                "avg_price": 0,
                "avg_reviews": 0,
                "avg_rating": 0,
                "unique_sellers": 0,
                "ozon_self_count": 0,
                "ozon_self_ratio": 0,
                "price_min": 0,
                "price_max": 0,
                "price_std": 0,
                "price_concentration": 0,
                "low_rating_ratio": 0,
                "products": [],
                "error": "无数据",
            }

        # 价格统计
        prices = [p["price"] for p in products if p.get("price", 0) > 0]
        avg_price = sum(prices) / len(prices) if prices else 0
        price_min = min(prices) if prices else 0
        price_max = max(prices) if prices else 0
        price_std = (sum((p - avg_price) ** 2 for p in prices) / len(prices)) ** 0.5 if prices else 0
        price_concentration = price_std / avg_price if avg_price > 0 else 0

        # 评论统计
        reviews = [p.get("reviews", 0) for p in products]
        avg_reviews = sum(reviews) / len(reviews) if reviews else 0

        # 评分统计
        ratings = [p.get("rating", 0) for p in products if p.get("rating", 0) > 0]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        low_rating_ratio = len([r for r in ratings if r < 4.0]) / len(ratings) if ratings else 0

        # 卖家统计
        sellers = [p.get("seller", "") for p in products if p.get("seller")]
        unique_sellers = len(set(sellers))
        ozon_self_count = len([p for p in products if p.get("is_ozon_self", False)])
        ozon_self_ratio = ozon_self_count / len(products) if products else 0

        # TOP10统计（前10个商品的指标）
        top10 = products[:10]
        top10_avg_reviews = sum(p.get("reviews", 0) for p in top10) / len(top10) if top10 else 0
        top10_avg_rating = sum(p.get("rating", 0) for p in top10 if p.get("rating", 0) > 0) / max(1, len([p for p in top10 if p.get("rating", 0) > 0]))
        top10_ozon_self = len([p for p in top10 if p.get("is_ozon_self", False)])

        return {
            "keyword_ru": keyword_ru,
            "keyword_en": keyword_en,
            "timestamp": datetime.now().isoformat(),
            "total_search_results": total_results,
            "scraped_products": len(products),
            # 全量统计
            "avg_price": round(avg_price, 2),
            "avg_reviews": round(avg_reviews, 2),
            "avg_rating": round(avg_rating, 2),
            "unique_sellers": unique_sellers,
            "ozon_self_count": ozon_self_count,
            "ozon_self_ratio": round(ozon_self_ratio, 4),
            "price_min": price_min,
            "price_max": price_max,
            "price_std": round(price_std, 2),
            "price_concentration": round(price_concentration, 4),
            "low_rating_ratio": round(low_rating_ratio, 4),
            # TOP10统计（蓝海评分核心数据）
            "top10_avg_reviews": round(top10_avg_reviews, 2),
            "top10_avg_rating": round(top10_avg_rating, 2),
            "top10_ozon_self_count": top10_ozon_self,
            "top10_seller_count": len(set(p.get("seller", "") for p in top10 if p.get("seller"))),
            # 价格分布（5个区间）
            "price_distribution": self._price_distribution(prices),
            # 原始商品数据
            "products": products,
        }

    def _price_distribution(self, prices):
        """计算价格区间分布"""
        if not prices:
            return {}

        ranges = {
            "≤300₽": (0, 300),
            "300-500₽": (300, 500),
            "500-1000₽": (500, 1000),
            "1000-1500₽": (1000, 1500),
            "≥1500₽": (1500, float("inf")),
        }

        dist = {}
        for label, (lo, hi) in ranges.items():
            count = len([p for p in prices if lo <= p < hi])
            dist[label] = {
                "count": count,
                "ratio": round(count / len(prices), 4),
            }
        return dist

    async def _random_delay(self, min_s, max_s):
        """随机延迟，模拟人类行为"""
        delay = random.uniform(min_s, max_s)
        await self.page.wait_for_timeout(int(delay * 1000))


async def run_monitoring():
    """执行一次完整监控任务"""
    print("=" * 60)
    print(f"🚀 Ozon蓝海自动监控 — 开始执行")
    print(f"   时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   关键词数量: {len(MONITOR_KEYWORDS)}")
    print("=" * 60)

    scraper = OzonScraper(
        headless=SCRAPER_CONFIG["headless"],
        use_stealth=SCRAPER_CONFIG["use_stealth"],
    )

    await scraper.init_browser()

    results = []
    for i, kw in enumerate(MONITOR_KEYWORDS):
        print(f"\n--- [{i+1}/{len(MONITOR_KEYWORDS)}] {kw['category']} ---")

        result = await scraper.scrape_keyword(
            keyword_ru=kw["keyword_ru"],
            keyword_en=kw["keyword_en"],
            max_pages=SCRAPER_CONFIG["max_pages"],
        )

        # 添加品类元数据
        result["category"] = kw["category"]
        result["tags"] = kw["tags"]

        results.append(result)

        # 关键词间延迟
        if i < len(MONITOR_KEYWORDS) - 1:
            delay = SCRAPER_CONFIG["keyword_delay"] + random.uniform(0, 5)
            print(f"   ⏳ 等待 {delay:.1f} 秒...")
            await scraper.page.wait_for_timeout(int(delay * 1000))

    await scraper.close_browser()

    # 保存数据
    save_results(results)
    print("\n" + "=" * 60)
    print("✅ 监控任务完成！")
    print("=" * 60)

    return results


def save_results(results):
    """保存监控结果到JSON文件"""
    timestamp = datetime.now()
    output = {
        "timestamp": timestamp.isoformat(),
        "date": timestamp.strftime("%Y-%m-%d"),
        "time": timestamp.strftime("%H:%M:%S"),
        "keywords_count": len(results),
        "results": results,
    }

    # 保存最新数据
    latest_path = PROJECT_ROOT / DATA_CONFIG["latest_file"]
    with open(latest_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"💾 最新数据已保存: {latest_path}")

    # 保存历史数据
    history_path = PROJECT_ROOT / DATA_CONFIG["history_dir"] / f"{timestamp.strftime('%Y-%m-%d_%H-%M')}.json"
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"💾 历史数据已保存: {history_path}")

    # 保存仪表盘专用数据（精简版，去掉products原始数据）
    dashboard_output = {
        "timestamp": timestamp.isoformat(),
        "date": timestamp.strftime("%Y-%m-%d"),
        "time": timestamp.strftime("%H:%M:%S"),
        "categories": [],
    }
    for r in results:
        cat_data = {
            "keyword_ru": r["keyword_ru"],
            "keyword_en": r["keyword_en"],
            "category": r.get("category", ""),
            "tags": r.get("tags", []),
            "total_search_results": r["total_search_results"],
            "scraped_products": r["scraped_products"],
            "avg_price": r["avg_price"],
            "avg_reviews": r["avg_reviews"],
            "avg_rating": r["avg_rating"],
            "unique_sellers": r["unique_sellers"],
            "ozon_self_ratio": r["ozon_self_ratio"],
            "price_concentration": r["price_concentration"],
            "low_rating_ratio": r["low_rating_ratio"],
            "top10_avg_reviews": r["top10_avg_reviews"],
            "top10_avg_rating": r["top10_avg_rating"],
            "top10_ozon_self_count": r["top10_ozon_self_count"],
            "top10_seller_count": r["top10_seller_count"],
            "price_min": r["price_min"],
            "price_max": r["price_max"],
            "price_distribution": r.get("price_distribution", {}),
        }
        dashboard_output["categories"].append(cat_data)

    dashboard_path = PROJECT_ROOT / DATA_CONFIG["dashboard_file"]
    with open(dashboard_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_output, f, ensure_ascii=False, indent=2)
    print(f"💾 仪表盘数据已保存: {dashboard_path}")


# ============================================================
# 离线模式：不爬取Ozon，仅用模拟数据演示Dashboard
# ============================================================
def generate_demo_data():
    """生成演示数据（用于开发测试Dashboard，不需要真正爬取Ozon）"""
    print("📝 生成演示数据（离线模式）...")

    timestamp = datetime.now()

    demo_results = []
    for kw in MONITOR_KEYWORDS:
        # 为每个品类生成合理的模拟数据
        is_red_ocean = "红海对照" in kw.get("tags", [])
        is_explore = "探索" in kw.get("tags", [])

        if is_red_ocean:
            # 红海品类：高竞争、高评论、低利润
            total_results = random.randint(5000, 20000)
            avg_reviews = random.randint(800, 3000)
            avg_rating = random.uniform(4.0, 4.5)
            unique_sellers = random.randint(40, 100)
            ozon_self_ratio = random.uniform(0.15, 0.35)
            price_concentration = random.uniform(0.05, 0.15)
            low_rating_ratio = random.uniform(0.05, 0.12)
            top10_avg_reviews = random.randint(500, 2000)
            top10_seller_count = random.randint(15, 30)
            top10_ozon_self_count = random.randint(2, 5)
        elif is_explore:
            # 探索品类：中等竞争、不确定需求
            total_results = random.randint(50, 300)
            avg_reviews = random.randint(10, 80)
            avg_rating = random.uniform(4.2, 4.7)
            unique_sellers = random.randint(3, 8)
            ozon_self_ratio = random.uniform(0, 0.05)
            price_concentration = random.uniform(0.3, 0.5)
            low_rating_ratio = random.uniform(0.15, 0.25)
            top10_avg_reviews = random.randint(5, 30)
            top10_seller_count = random.randint(3, 6)
            top10_ozon_self_count = random.randint(0, 1)
        else:
            # 蓝海品类：低竞争、高机会
            total_results = random.randint(100, 800)
            avg_reviews = random.randint(15, 150)
            avg_rating = random.uniform(4.3, 4.8)
            unique_sellers = random.randint(5, 15)
            ozon_self_ratio = random.uniform(0, 0.08)
            price_concentration = random.uniform(0.35, 0.6)
            low_rating_ratio = random.uniform(0.15, 0.3)
            top10_avg_reviews = random.randint(10, 100)
            top10_seller_count = random.randint(3, 10)
            top10_ozon_self_count = random.randint(0, 2)

        # 价格根据品类调整
        if "车载" in kw["category"] or "冬季" in kw["category"]:
            avg_price = random.randint(800, 2500)
            price_min = random.randint(300, 500)
            price_max = random.randint(3000, 5000)
        elif "3C" in kw["category"]:
            avg_price = random.randint(150, 400)
            price_min = random.randint(50, 100)
            price_max = random.randint(500, 1500)
        else:
            avg_price = random.randint(300, 1000)
            price_min = random.randint(100, 250)
            price_max = random.randint(1500, 3000)

        result = {
            "keyword_ru": kw["keyword_ru"],
            "keyword_en": kw["keyword_en"],
            "category": kw["category"],
            "tags": kw["tags"],
            "timestamp": timestamp.isoformat(),
            "total_search_results": total_results,
            "scraped_products": random.randint(20, 100),
            "avg_price": avg_price,
            "avg_reviews": avg_reviews,
            "avg_rating": round(avg_rating, 2),
            "unique_sellers": unique_sellers,
            "ozon_self_count": int(unique_sellers * ozon_self_ratio),
            "ozon_self_ratio": round(ozon_self_ratio, 4),
            "price_min": price_min,
            "price_max": price_max,
            "price_std": round(random.uniform(100, 500), 2),
            "price_concentration": round(price_concentration, 4),
            "low_rating_ratio": round(low_rating_ratio, 4),
            "top10_avg_reviews": top10_avg_reviews,
            "top10_avg_rating": round(avg_rating - random.uniform(0, 0.2), 2),
            "top10_ozon_self_count": top10_ozon_self_count,
            "top10_seller_count": top10_seller_count,
            "price_distribution": {
                "≤300₽": {"count": random.randint(2, 10), "ratio": round(random.uniform(0.05, 0.15), 4)},
                "300-500₽": {"count": random.randint(5, 15), "ratio": round(random.uniform(0.1, 0.25), 4)},
                "500-1000₽": {"count": random.randint(8, 20), "ratio": round(random.uniform(0.2, 0.35), 4)},
                "1000-1500₽": {"count": random.randint(3, 10), "ratio": round(random.uniform(0.05, 0.2), 4)},
                "≥1500₽": {"count": random.randint(2, 8), "ratio": round(random.uniform(0.05, 0.15), 4)},
            },
            "products": [],
        }
        demo_results.append(result)

    save_results(demo_results)
    print("✅ 演示数据已生成并保存！")
    return demo_results


# ============================================================
# 主入口
# ============================================================
def main():
    """主入口"""
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # 离线模式：生成演示数据
        generate_demo_data()
        return

    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
Ozon蓝海自动监控系统

用法:
  python monitor.py          # 正常模式：爬取Ozon实时数据
  python monitor.py --demo   # 离线模式：生成演示数据（用于测试Dashboard）
  python monitor.py --help   # 显示帮助信息

注意:
  - 正常模式需要安装 Playwright: pip install playwright && playwright install chromium
  - 建议每天运行一次，北京时间06:00（莫斯科01:00，流量低谷）
  - 可通过 Windows 任务计划程序设置自动定时运行
""")
        return

    # 正常模式：异步爬取
    import asyncio
    asyncio.run(run_monitoring())


if __name__ == "__main__":
    main()
