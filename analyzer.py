"""
Ozon蓝海自动监控系统 — 分析引擎
读取爬取数据，计算蓝海评分、趋势变化、生成告警
"""

import json
import os
from datetime import datetime
from pathlib import Path

from config import SCORING_THRESHOLDS, BLUE_OCEAN_THRESHOLD, ALERT_CONFIG, DATA_CONFIG

PROJECT_ROOT = Path(__file__).parent


class BlueOceanAnalyzer:
    """蓝海评分分析引擎"""

    def analyze_category(self, category_data):
        """
        对单个品类计算蓝海评分（7维度，满分10分）
        返回: {score, dimensions, recommendation, alerts}
        """
        dimensions = {}

        # 1. 搜索结果数（代理搜索需求）
        total_results = category_data.get("total_search_results", 0)
        if total_results >= 100:
            dimensions["search_volume"] = SCORING_THRESHOLDS["search_results"]["high"]
        elif total_results >= 30:
            dimensions["search_volume"] = SCORING_THRESHOLDS["search_results"]["medium"]
        else:
            dimensions["search_volume"] = SCORING_THRESHOLDS["search_results"]["low"]
        dimensions["search_volume_detail"] = f"搜索结果{total_results}个"

        # 2. TOP10平均评论数
        top10_reviews = category_data.get("top10_avg_reviews", 0)
        if top10_reviews < 200:
            dimensions["avg_reviews"] = SCORING_THRESHOLDS["avg_reviews"]["high"]
        elif top10_reviews < 500:
            dimensions["avg_reviews"] = SCORING_THRESHOLDS["avg_reviews"]["medium"]
        else:
            dimensions["avg_reviews"] = SCORING_THRESHOLDS["avg_reviews"]["low"]
        dimensions["avg_reviews_detail"] = f"TOP10平均评论{top10_reviews}条"

        # 3. TOP10卖家数
        top10_sellers = category_data.get("top10_seller_count", 0)
        if top10_sellers < 10:
            dimensions["seller_count"] = SCORING_THRESHOLDS["seller_count"]["high"]
        elif top10_sellers < 20:
            dimensions["seller_count"] = SCORING_THRESHOLDS["seller_count"]["medium"]
        else:
            dimensions["seller_count"] = SCORING_THRESHOLDS["seller_count"]["low"]
        dimensions["seller_count_detail"] = f"TOP10卖家{top10_sellers}家"

        # 4. Ozon自营占比
        ozon_ratio = category_data.get("ozon_self_ratio", 0)
        if ozon_ratio < 0.10:
            dimensions["ozon_self"] = SCORING_THRESHOLDS["ozon_self_ratio"]["high"]
        elif ozon_ratio < 0.30:
            dimensions["ozon_self"] = SCORING_THRESHOLDS["ozon_self_ratio"]["medium"]
        else:
            dimensions["ozon_self"] = SCORING_THRESHOLDS["ozon_self_ratio"]["low"]
        dimensions["ozon_self_detail"] = f"自营占比{ozon_ratio*100:.1f}%"

        # 5. 价格集中度
        price_conc = category_data.get("price_concentration", 0)
        if price_conc > 0.4:
            dimensions["price_concentration"] = SCORING_THRESHOLDS["price_concentration"]["high"]
        elif price_conc > 0.2:
            dimensions["price_concentration"] = SCORING_THRESHOLDS["price_concentration"]["medium"]
        else:
            dimensions["price_concentration"] = SCORING_THRESHOLDS["price_concentration"]["low"]
        dimensions["price_concentration_detail"] = f"价格集中度{price_conc:.2f}"

        # 6. 低评分比例（差评=差异化机会）
        low_rating_ratio = category_data.get("low_rating_ratio", 0)
        if low_rating_ratio > 0.20:
            dimensions["rating_variance"] = SCORING_THRESHOLDS["rating_variance"]["high"]
        elif low_rating_ratio > 0.10:
            dimensions["rating_variance"] = SCORING_THRESHOLDS["rating_variance"]["medium"]
        else:
            dimensions["rating_variance"] = SCORING_THRESHOLDS["rating_variance"]["low"]
        dimensions["rating_variance_detail"] = f"低评分占比{low_rating_ratio*100:.1f}%"

        # 7. rFBS物流适配度（从品类标签推算）
        tags = category_data.get("tags", [])
        if "轻小件" in tags and "需EAC" not in tags and "需备货" not in tags:
            dimensions["rFBS_fitness"] = SCORING_THRESHOLDS["rFBS_fitness"]["high"]
        elif "中等体积" in tags or "需简单认证" in tags:
            dimensions["rFBS_fitness"] = SCORING_THRESHOLDS["rFBS_fitness"]["medium"]
        else:
            dimensions["rFBS_fitness"] = SCORING_THRESHOLDS["rFBS_fitness"]["low"]
        dimensions["rFBS_fitness_detail"] = f"标签: {', '.join(tags)}"

        # 计算总分（只取数值维度，排除_detail字符串）
        score_keys = ["search_volume", "avg_reviews", "seller_count", "ozon_self",
                       "price_concentration", "rating_variance", "rFBS_fitness"]
        total_score = sum(dimensions.get(k, 0) for k in score_keys)

        # 推荐级别
        if total_score >= BLUE_OCEAN_THRESHOLD["strong_recommend"]:
            recommendation = "🔥 强烈推荐入场"
        elif total_score >= BLUE_OCEAN_THRESHOLD["conditional"]:
            recommendation = "🌊 有条件入场（需差异化）"
        else:
            recommendation = "❌ 建议放弃"

        return {
            "category": category_data.get("category", ""),
            "keyword_ru": category_data.get("keyword_ru", ""),
            "keyword_en": category_data.get("keyword_en", ""),
            "tags": tags,
            "total_score": total_score,
            "dimensions": dimensions,
            "recommendation": recommendation,
            # 保留核心数据指标
            "metrics": {
                "total_search_results": total_results,
                "avg_price": category_data.get("avg_price", 0),
                "avg_reviews": category_data.get("avg_reviews", 0),
                "avg_rating": category_data.get("avg_rating", 0),
                "unique_sellers": category_data.get("unique_sellers", 0),
                "ozon_self_ratio": ozon_ratio,
                "price_concentration": price_conc,
                "low_rating_ratio": low_rating_ratio,
                "top10_avg_reviews": top10_reviews,
                "top10_avg_rating": category_data.get("top10_avg_rating", 0),
                "top10_seller_count": top10_sellers,
                "price_min": category_data.get("price_min", 0),
                "price_max": category_data.get("price_max", 0),
            },
        }

    def analyze_all(self, results_data):
        """对所有品类进行蓝海评分分析"""
        categories = results_data.get("categories", results_data.get("results", []))
        analyses = []

        for cat_data in categories:
            analysis = self.analyze_category(cat_data)
            analyses.append(analysis)

        # 按评分排序（高分在前）
        analyses.sort(key=lambda x: x["total_score"], reverse=True)

        return analyses

    def detect_alerts(self, current_analyses, previous_data=None):
        """检测告警信号"""
        alerts = []

        if not previous_data:
            # 第一次运行，没有历史数据
            for analysis in current_analyses:
                if analysis["total_score"] >= BLUE_OCEAN_THRESHOLD["strong_recommend"]:
                    alerts.append({
                        "type": "🟢 新蓝海发现",
                        "category": analysis["category"],
                        "message": f"「{analysis['category']}」蓝海评分{analysis['total_score']}分，强烈推荐入场！",
                        "score": analysis["total_score"],
                        "priority": "high",
                    })
            return alerts

        # 对比历史数据
        previous_analyses = previous_data.get("analyses", [])
        prev_map = {a["category"]: a for a in previous_analyses}

        for analysis in current_analyses:
            cat_name = analysis["category"]
            prev = prev_map.get(cat_name)

            if not prev:
                continue

            prev_score = prev.get("total_score", 0)
            curr_score = analysis["total_score"]

            # 新蓝海出现
            if ALERT_CONFIG["new_blue_ocean"]:
                if prev_score < BLUE_OCEAN_THRESHOLD["conditional"] and curr_score >= BLUE_OCEAN_THRESHOLD["strong_recommend"]:
                    alerts.append({
                        "type": "🟢 新蓝海出现",
                        "category": cat_name,
                        "message": f"「{cat_name}」从{prev_score}分跃升到{curr_score}分，变成蓝海品类！",
                        "priority": "high",
                    })

            # 蓝海变红海
            if ALERT_CONFIG["blue_to_red"]:
                if prev_score >= BLUE_OCEAN_THRESHOLD["strong_recommend"] and curr_score < BLUE_OCEAN_THRESHOLD["conditional"]:
                    alerts.append({
                        "type": "🔴 蓝海变红海",
                        "category": cat_name,
                        "message": f"「{cat_name}」从{prev_score}分降至{curr_score}分，竞争加剧，建议评估是否退出！",
                        "priority": "high",
                    })

            # 评论数暴增
            if ALERT_CONFIG["review_explosion"]:
                prev_reviews = prev.get("metrics", {}).get("top10_avg_reviews", 0)
                curr_reviews = analysis["metrics"]["top10_avg_reviews"]
                if prev_reviews > 0 and curr_reviews > prev_reviews * 1.3:
                    alerts.append({
                        "type": "⚠️ 评论暴增",
                        "category": cat_name,
                        "message": f"「{cat_name}」TOP10评论从{prev_reviews}增长到{curr_reviews}（+{(curr_reviews/prev_reviews-1)*100:.0f}%），竞争正在加剧",
                        "priority": "medium",
                    })

            # 自营介入
            if ALERT_CONFIG["ozon_self_entry"]:
                prev_self = prev.get("metrics", {}).get("ozon_self_ratio", 0)
                curr_self = analysis["metrics"]["ozon_self_ratio"]
                if prev_self < 0.10 and curr_self > 0.30:
                    alerts.append({
                        "type": "🟠 自营介入",
                        "category": cat_name,
                        "message": f"「{cat_name}」Ozon自营占比从{prev_self*100:.1f}%升至{curr_self*100:.1f}%，自营开始主导该品类",
                        "priority": "medium",
                    })

            # 价格战加剧
            if ALERT_CONFIG["price_war"]:
                prev_conc = prev.get("metrics", {}).get("price_concentration", 0)
                curr_conc = analysis["metrics"]["price_concentration"]
                if prev_conc > 0.4 and curr_conc < 0.2:
                    alerts.append({
                        "type": "🟡 价格战加剧",
                        "category": cat_name,
                        "message": f"「{cat_name}」价格集中度从{prev_conc:.2f}降至{curr_conc:.2f}，卖家正在打价格战",
                        "priority": "medium",
                    })

        # 按优先级排序
        priority_order = {"high": 0, "medium": 1, "low": 2}
        alerts.sort(key=lambda a: priority_order.get(a["priority"], 3))

        return alerts

    def generate_dashboard_data(self, analyses, alerts=None, raw_results=None):
        """生成Dashboard专用数据"""
        # 蓝海指数排行
        ranking = []
        
        # 构建 market_intel 索引（从原始数据中提取）
        intel_map = {}
        if raw_results:
            for r in raw_results:
                cat = r.get("category", "")
                if "market_intel" in r:
                    intel_map[cat] = r["market_intel"]

        for a in analyses:
            # 计算蓝海指数 = 搜索结果数 / (卖家数 + 1)
            search_results = a["metrics"]["total_search_results"]
            sellers = a["metrics"]["unique_sellers"]
            blue_ocean_index = search_results / (sellers + 1) if sellers > 0 else search_results

            entry = {
                "category": a["category"],
                "keyword_ru": a["keyword_ru"],
                "keyword_en": a["keyword_en"],
                "tags": a["tags"],
                "total_score": a["total_score"],
                "recommendation": a["recommendation"],
                "blue_ocean_index": round(blue_ocean_index, 2),
                "dimensions": a["dimensions"],
                "metrics": a["metrics"],
            }
            # 附加市场情报
            if a["category"] in intel_map:
                entry["market_intel"] = intel_map[a["category"]]
            ranking.append(entry)

        return {
            "timestamp": datetime.now().isoformat(),
            "ranking": ranking,
            "alerts": alerts or [],
            "summary": {
                "total_categories": len(analyses),
                "strong_recommend": len([a for a in analyses if a["total_score"] >= BLUE_OCEAN_THRESHOLD["strong_recommend"]]),
                "conditional": len([a for a in analyses if BLUE_OCEAN_THRESHOLD["conditional"] <= a["total_score"] < BLUE_OCEAN_THRESHOLD["strong_recommend"]]),
                "avoid": len([a for a in analyses if a["total_score"] < BLUE_OCEAN_THRESHOLD["conditional"]]),
                "avg_score": round(sum(a["total_score"] for a in analyses) / len(analyses), 2) if analyses else 0,
            },
        }


def run_analysis():
    """执行分析任务"""
    print("\n📊 开始蓝海评分分析...")

    analyzer = BlueOceanAnalyzer()

    # 读取最新数据
    latest_path = PROJECT_ROOT / DATA_CONFIG["latest_file"]
    if not latest_path.exists():
        print("❌ 未找到最新数据文件，请先运行 monitor.py")
        return None

    with open(latest_path, "r", encoding="utf-8") as f:
        current_data = json.load(f)

    # 分析所有品类
    analyses = analyzer.analyze_all(current_data)

    # 读取历史数据（用于对比和告警）
    previous_data = None
    history_dir = PROJECT_ROOT / DATA_CONFIG["history_dir"]
    history_files = sorted(history_dir.glob("*.json"))
    if len(history_files) >= 2:
        # 取最近的一次历史数据（排除当前）
        prev_file = history_files[-2]
        with open(prev_file, "r", encoding="utf-8") as f:
            prev_raw = json.load(f)
        # 如果有之前保存的分析结果，直接用
        prev_analysis_path = PROJECT_ROOT / "data" / "analysis_history" / f"{prev_file.stem}_analysis.json"
        if prev_analysis_path.exists():
            with open(prev_analysis_path, "r", encoding="utf-8") as f:
                previous_data = json.load(f)
        else:
            previous_data = {"analyses": analyzer.analyze_all(prev_raw)}

    # 检测告警
    alerts = analyzer.detect_alerts(analyses, previous_data)

    # 生成Dashboard数据（传入原始数据以保留market_intel）
    raw_results = current_data.get("results", [])
    dashboard_data = analyzer.generate_dashboard_data(analyses, alerts, raw_results)

    # 保存分析结果
    analysis_dir = PROJECT_ROOT / "data" / "analysis_history"
    analysis_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now()
    analysis_path = analysis_dir / f"{timestamp.strftime('%Y-%m-%d_%H-%M')}_analysis.json"
    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
    print(f"💾 分析结果已保存: {analysis_path}")

    # 更新Dashboard数据文件
    dashboard_path = PROJECT_ROOT / DATA_CONFIG["dashboard_file"]
    with open(dashboard_path, "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)
    print(f"💾 Dashboard数据已更新: {dashboard_path}")

    # 输出排名
    print("\n" + "=" * 60)
    print("📊 蓝海品类排名")
    print("=" * 60)
    for i, a in enumerate(analyses[:10]):
        print(f"  {i+1}. [{a['total_score']}分] {a['recommendation']} — {a['category']}")

    if alerts:
        print("\n" + "=" * 60)
        print("🔔 告警通知")
        print("=" * 60)
        for alert in alerts:
            print(f"  {alert['type']} {alert['message']}")

    return dashboard_data


def main():
    """主入口"""
    run_analysis()


if __name__ == "__main__":
    main()
