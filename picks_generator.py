"""
Ozon选品数据生成器
基于公开市场数据和监控数据，生成结构化选品JSON供Dashboard使用

与config.py的关键区别：
- config.py: 预先硬编码36个品类及其标签（主观预设）
- picks_generator.py: 基于实际采集的市场数据（WebSearch结果、趋势报告）生成选品建议

数据来源优先级：
1. Ozon官方公开数据（季度报告、搜索趋势）
2. 电商行业媒体报道（亿恩网、和讯网等）
3. 国内货源平台数据（1688搜索）
4. 本地监控数据（data/latest.json）
"""

import json
import os
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


class PicksGenerator:
    """选品数据生成器 — 基于真实市场数据"""

    def __init__(self):
        self.data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "updated": datetime.now().isoformat(),
            "data_source": "基于公开市场数据生成 — Ozon官方报告、行业媒体、1688货源",
            "market_context": {},
            "market_trends": [],
            "picks": [],
            "red_ocean_warning": [],
            "action_items": [],
            "upcoming_alerts": [],
        }

    def set_market_context(self, context: dict):
        """设置市场背景信息"""
        self.data["market_context"] = context

    def add_market_trend(self, trend: dict):
        """添加市场趋势数据点"""
        self.data["market_trends"].append(trend)

    def add_pick(self, pick: dict):
        """
        添加选品推荐

        pick格式:
        {
            "rank": int,
            "category": "品类名",
            "sub_category": "子品类",
            "keyword_ru": "俄语搜索词",
            "priority": "推荐等级",
            "reasoning": "分析理由",
            "ozon_search_url": "Ozon搜索结果页URL",
            "ozon_competitor_url": "竞品分析URL(可选)",
            "market_data": {
                "sales_growth": "销量增长数据",
                "season": "季节",
                "competition_level": "竞争程度",
                "commission": "佣金比例",
                "logistics_type": "物流类型"
            },
            "sourcing": {
                "platform": "货源平台",
                "search_keyword": "搜索关键词",
                "search_url": "货源搜索URL",
                "price_range_cny": "人民币价格区间",
                "suggested_ozon_price": "建议Ozon售价(卢布)",
                "suggested_ozon_price_cny": "建议Ozon售价(人民币)",
                "profit_estimate": "利润预估",
                "suppliers_count": "供应商数量",
                "quality_tips": "品质建议",
                "backup_platform": "备选平台",
                "backup_search_url": "备选搜索URL"
            }
        }
        """
        self.data["picks"].append(pick)

    def add_red_ocean(self, category: str, keyword_ru: str, reason: str):
        """添加红海警告"""
        self.data["red_ocean_warning"].append({
            "category": category,
            "keyword_ru": keyword_ru,
            "reason": reason,
            "verdict": "不推荐入场"
        })

    def add_action_item(self, priority: str, action: str, detail: str = ""):
        """添加行动建议"""
        self.data["action_items"].append({
            "priority": priority,
            "action": action,
            "detail": detail
        })

    def add_upcoming_alert(self, date: str, event: str):
        """添加即将到来的事件提醒"""
        self.data["upcoming_alerts"].append({
            "date": date,
            "event": event
        })

    def save(self, filepath: str = None):
        """保存选品数据到JSON"""
        if filepath is None:
            filepath = PROJECT_ROOT / "daily-picks" / "latest-picks.json"

        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

        print(f"选品数据已保存: {filepath}")
        return str(filepath)

    @staticmethod
    def build_ozon_search_url(keyword_ru: str, sort_by: str = "rating") -> str:
        """根据俄语关键词生成Ozon搜索URL"""
        from urllib.parse import quote
        encoded = quote(keyword_ru, safe="")
        return f"https://www.ozon.ru/search/?text={encoded}&sorting={sort_by}"

    @staticmethod
    def build_1688_search_url(keyword: str) -> str:
        """根据中文关键词生成1688搜索URL（GBK编码，s.1688.com要求）

        注意：s.1688.com 的 keywords 参数必须使用 GBK 编码，
        使用 UTF-8 编码会导致搜索框中文乱码。
        """
        from urllib.parse import quote
        # encoding='gbk' 是关键 — 1688老接口只认识GBK
        encoded = quote(keyword, safe="", encoding="gbk")
        return f"https://s.1688.com/selloffer/offer_search.htm?keywords={encoded}&n=y"


def generate_daily_picks_template():
    """
    生成日报模板 — 供自动化任务使用

    自动化任务（WebSearch + assistant）负责填充实际数据，
    此函数提供数据结构和辅助URL生成方法。
    """
    gen = PicksGenerator()

    # 示例：构建市场背景
    gen.set_market_context({
        "ozon_overview": "待填充：Ozon当前宏观数据",
        "current_season": "待填充：当前季节特征",
        "next_season": "待填充：下个季节准备"
    })

    print("PicksGenerator 就绪")
    print("用法示例:")
    print("  gen = PicksGenerator()")
    print("  gen.add_pick({...})")
    print("  gen.save()")
    return gen


if __name__ == "__main__":
    generate_daily_picks_template()
