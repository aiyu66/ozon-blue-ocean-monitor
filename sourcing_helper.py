#!/usr/bin/env python3
"""
Ozon选品辅助脚本 — 1688/拼多多货源链接生成器
用途：读取蓝海监控数据，为高评分品类生成国内货源搜索链接

使用方法：
  python sourcing_helper.py

输出：在 sourcing/ 目录下生成今日选品清单，包含可直接点击的搜索链接
"""

import json
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

def ensure_dir(path):
    path.mkdir(parents=True, exist_ok=True)
    return path

def load_monitor_data():
    """读取最新监控数据"""
    latest_path = PROJECT_ROOT / "data" / "latest.json"
    if not latest_path.exists():
        print("未找到监控数据，请先运行 monitor.py 或 run.py")
        return None
    with open(latest_path, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_1688_search_url(keyword_cn):
    """生成1688搜索链接"""
    import urllib.parse
    encoded = urllib.parse.quote(keyword_cn)
    return f"https://s.1688.com/selloffer/offer_search.htm?keywords={encoded}&n=y&netType=1%2C11&sortType=va_rmdank_desc"

def generate_pdd_search_url(keyword_cn):
    """生成拼多多搜索链接（通过浏览器搜索）"""
    import urllib.parse
    encoded = urllib.parse.quote(keyword_cn)
    return f"https://mobile.yangkeduo.com/search_result.html?search_key={encoded}"

def analyze_and_generate(data):
    """分析数据并生成选品清单"""
    from analyzer import BlueOceanAnalyzer

    analyzer = BlueOceanAnalyzer()
    analyses = analyzer.analyze_all(data)

    # 筛选高评分品类
    strong = [a for a in analyses if a["total_score"] >= 7]
    conditional = [a for a in analyses if 5 <= a["total_score"] < 7]

    # 中文关键词映射（用于1688搜索）
    CN_KEYWORDS = {
        "автоматическая кормушка для кошек": "自动喂食器 猫",
        "автокормушка для собак малых пород": "自动喂食器 小型犬",
        "поилка для кошек автоматическая": "猫咪饮水机 自动",
        "игрушка для кошек интерактивная": "猫玩具 互动",
        "держатель для туалета кошки": "猫砂盆 支架",
        "щетка для удаления шерсти": "宠物除毛刷",
        "органайзер для холодильника": "冰箱收纳盒",
        "контейнеры для специй": "调料瓶 调料罐",
        "полка складная для ванной": "浴室折叠置物架",
        "сушилка для посуды компактная": "迷你沥水架",
        "термометр для мяса электронный": "食物温度计 电子",
        "многофункциональная терка для овощей": "多功能切菜器",
        "дозатор для мыла автоматический": "自动皂液器",
        "держатель для телефона в авто с зарядкой": "车载手机支架 无线充电",
        "автоодеяло с подогревом": "车载加热毯",
        "ароматизатор для авто деревянный": "木质车载香薰",
        "органайзер для багажника авто": "汽车后备箱收纳箱",
        "чехол на руль ледяной": "冰丝方向盘套",
        "умный браслет фитнес": "智能手环 健身",
        "часы детские с GPS трекером": "儿童GPS手表",
        "кольцо умное для здоровья": "智能健康戒指",
        "садовые ножницы": "修枝剪 园艺剪刀",
        "набор инструментов для сада мини": "迷你园艺工具套装",
        "светильник для растений LED": "LED植物生长灯",
        "фонарь солнечный для сада": "太阳能庭院灯",
        "гамак портативный": "便携吊床",
        "магнитные блоки для детей": "儿童磁力片",
        "набор для каллиграфии": "书法套装",
        "набор научных экспериментов для детей": "儿童科学实验套装",
        "конструктор деревянный": "木质积木",
        "репеллент от комаров портативный": "驱蚊手环 便携驱蚊器",
        "веер USB портативный": "USB小风扇 便携",
        "солнцезащитная шапка рыбака": "防晒渔夫帽",
        "портативный обогреватель для рук": "暖手宝 便携",
        "перчатки с подогревом USB": "USB加热手套",
        "свеча ароматическая в подарке": "香薰蜡烛礼盒",
        "гирлянда новогодняя LED": "LED新年灯串",
        "чехол для телефона": "手机壳",
        "зимняя одежда для собак": "狗冬装",
        "наушники беспроводные": "无线耳机",
    }

    today = datetime.now().strftime("%Y-%m-%d")
    output_dir = ensure_dir(PROJECT_ROOT / "sourcing")
    output_path = output_dir / f"{today}-sourcing.md"

    lines = [
        f"# Ozon选品货源清单 — {today}",
        "",
        "> 本文件由 `sourcing_helper.py` 自动生成。包含可直接点击的1688/拼多多搜索链接。",
        "> 使用方式：点击链接 → 在浏览器中打开 → 筛选供应商 → 对比价格和质量 → 确定货源",
        "",
        "---",
        "",
    ]

    # 强烈推荐
    lines.append("## 🔥 强烈推荐上架（蓝海评分 ≥ 7分）")
    lines.append("")
    if strong:
        for a in strong:
            cat = a["category"]
            kw_ru = a["keyword_ru"]
            kw_cn = CN_KEYWORDS.get(kw_ru, a.get("keyword_en", "未知品类"))
            score = a["total_score"]
            metrics = a["metrics"]
            price_min = metrics.get("price_min", 0)
            price_max = metrics.get("price_max", 0)
            sellers = metrics.get("unique_sellers", 0)
            reviews = metrics.get("top10_avg_reviews", 0)

            lines.append(f"### {cat}（{score}分）")
            lines.append(f"- **Ozon价格区间**: {price_min}₽ - {price_max}₽")
            lines.append(f"- **卖家数**: {sellers} | **TOP10评论**: {reviews}")
            lines.append(f"- **1688搜索**: [{kw_cn}]({generate_1688_search_url(kw_cn)})")
            lines.append(f"- **拼多多搜索**: [{kw_cn}]({generate_pdd_search_url(kw_cn)})")
            lines.append("")
    else:
        lines.append("暂无评分≥7分的品类，查看「有条件入场」列表。")
        lines.append("")

    # 有条件入场
    lines.append("---")
    lines.append("")
    lines.append("## 🌊 有条件入场（评分 5-6分，需差异化）")
    lines.append("")
    if conditional:
        for a in conditional:
            cat = a["category"]
            kw_ru = a["keyword_ru"]
            kw_cn = CN_KEYWORDS.get(kw_ru, a.get("keyword_en", "未知品类"))
            score = a["total_score"]
            metrics = a["metrics"]
            price_min = metrics.get("price_min", 0)
            price_max = metrics.get("price_max", 0)
            sellers = metrics.get("unique_sellers", 0)
            reviews = metrics.get("top10_avg_reviews", 0)

            lines.append(f"### {cat}（{score}分）")
            lines.append(f"- **Ozon价格区间**: {price_min}₽ - {price_max}₽")
            lines.append(f"- **卖家数**: {sellers} | **TOP10评论**: {reviews}")
            lines.append(f"- **1688搜索**: [{kw_cn}]({generate_1688_search_url(kw_cn)})")
            lines.append(f"- **拼多多搜索**: [{kw_cn}]({generate_pdd_search_url(kw_cn)})")
            lines.append("")
    else:
        lines.append("暂无5-6分的品类。")
        lines.append("")

    # 选品建议
    lines.append("---")
    lines.append("")
    lines.append("## 💡 选品决策指南")
    lines.append("")
    lines.append('1. **优先选"强烈推荐"品类**：竞争低、需求明确，入场门槛低')
    lines.append("2. **对比Ozon和1688价差**：确保利润空间 ≥ 50%（扣除运费和佣金后）")
    lines.append("3. **看卖家数和评论数**：卖家数<10、评论数<200 = 真正的蓝海")
    lines.append("4. **选轻小件**：运费低、退货少、rFBS适配")
    lines.append("5. **避开自营占比>30%的品类**：Ozon自营介入深的品类难竞争")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print("\n" + "=" * 60)
    print("选品货源清单已生成: {}".format(output_path))
    print("   - 强烈推荐品类: {} 个".format(len(strong)))
    print("   - 有条件入场品类: {} 个".format(len(conditional)))
    print("   - 每个品类都附带了1688和拼多多的搜索链接")
    return output_path


def main():
    print("=" * 60)
    print("Ozon选品货源链接生成器")
    print("=" * 60)

    data = load_monitor_data()
    if not data:
        return

    output_path = analyze_and_generate(data)

    print("\n" + "=" * 60)
    print("使用建议")
    print("=" * 60)
    print("1. 打开生成的Markdown文件，里面有所有搜索链接")
    print("2. 点击1688链接，筛选供应商（优先选源头工厂）")
    print("3. 对比Ozon售价和1688成本价，计算利润空间")
    print("4. 确定货源后，用标签Listing生成器制作俄文Listing")
    print("5. 上架Ozon，开始测款")


if __name__ == "__main__":
    main()
