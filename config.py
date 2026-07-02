"""
Ozon蓝海自动监控系统 — 配置文件
定义监控关键词、评分阈值、调度参数等
"""

# ============================================================
# 监控关键词配置
# ============================================================
# 每个关键词组代表一个品类方向
# 结构: {关键词俄语, 关键词英语, 品类名称, 品类标签}

MONITOR_KEYWORDS = [
    # 🔥 第一梯队 — 强烈推荐（蓝海评分8-9分）
    {
        "keyword_ru": "садовые ножницы",
        "keyword_en": "pruning shears",
        "category": "园艺/达恰工具",
        "tags": ["蓝海", "旺季7-9月", "轻小件"],
    },
    {
        "keyword_ru": "инструменты для дачи",
        "keyword_en": "dacha tools",
        "category": "达恰用品",
        "tags": ["蓝海", "旺季5-8月", "轻小件"],
    },
    {
        "keyword_ru": "автоматическая кормушка для кошек",
        "keyword_en": "automatic cat feeder",
        "category": "宠物智能用品-猫",
        "tags": ["蓝海", "全年品", "轻小件"],
    },
    {
        "keyword_ru": " автокормушка для собак малых пород",
        "keyword_en": "small dog automatic feeder",
        "category": "宠物智能用品-小型犬",
        "tags": ["蓝海", "全年品", "轻小件"],
    },
    {
        "keyword_ru": "автоодеяло с подогревом",
        "keyword_en": "car heated blanket",
        "category": "车载冬季应急",
        "tags": ["蓝海", "旺季10-2月", "需备货"],
    },
    {
        "keyword_ru": "держатель для телефона в авто с зарядкой",
        "keyword_en": "car phone holder wireless charging",
        "category": "车载配件-手机支架",
        "tags": ["蓝海", "全年品", "轻小件"],
    },

    # 🌊 第二梯队 — 推荐（蓝海评分7分，需差异化）
    {
        "keyword_ru": "набор для каллиграфии",
        "keyword_en": "calligraphy set",
        "category": "俄语书法/教育用品",
        "tags": ["政策红利", "新需求", "轻小件"],
    },
    {
        "keyword_ru": "органайзер для холодильника",
        "keyword_en": "fridge organizer",
        "category": "家居收纳-冰箱收纳",
        "tags": ["刚需", "全年品", "轻小件"],
    },
    {
        "keyword_ru": "контейнеры для специй",
        "keyword_en": "spice containers",
        "category": "厨房小工具-调料瓶",
        "tags": ["刚需", "全年品", "轻小件"],
    },
    {
        "keyword_ru": "складная полка для кухни",
        "keyword_en": "foldable kitchen shelf",
        "category": "厨房收纳-折叠置物架",
        "tags": ["刚需", "全年品", "中等体积"],
    },

    # 🔍 探索性品类 — 需验证
    {
        "keyword_ru": "игрушка для кошек интерактивная",
        "keyword_en": "interactive cat toy",
        "category": "宠物玩具-互动类",
        "tags": ["探索", "复购率高", "轻小件"],
    },
    {
        "keyword_ru": "портативный обогреватель для рук",
        "keyword_en": "portable hand warmer",
        "category": "冬季保暖-暖手宝",
        "tags": ["探索", "旺季10-2月", "轻小件"],
    },
    {
        "keyword_ru": "перчатки с подогревом USB",
        "keyword_en": "USB heated gloves",
        "category": "冬季保暖-加热手套",
        "tags": ["探索", "旺季10-2月", "轻小件"],
    },
    {
        "keyword_ru": "набор инструментов для сада мини",
        "keyword_en": "mini garden tools set",
        "category": "达恰迷你园艺工具",
        "tags": ["蓝海", "旺季4-9月", "轻小件"],
    },

    # ❌ 红海对照 — 监控竞争激烈度变化
    {
        "keyword_ru": "чехол для телефона",
        "keyword_en": "phone case",
        "category": "3C配件-手机壳（红海对照）",
        "tags": ["红海对照", "超饱和", "不入场"],
    },
    {
        "keyword_ru": "зимняя одежда для собак",
        "keyword_en": "winter dog clothes",
        "category": "宠物保暖衣（红海对照）",
        "tags": ["红海对照", "退货率高", "不入场"],
    },
]

# ============================================================
# 蓝海评分阈值配置
# ============================================================
SCORING_THRESHOLDS = {
    # 月搜索量代理（用搜索结果商品数近似）
    "search_results": {
        "high": 2,     # 商品数>500 → 需求大但竞争也大
        "medium": 1,   # 商品数100-500
        "low": 0,      # 商品数<100 → 需求太小
    },
    # TOP10平均评论数
    "avg_reviews": {
        "high": 2,     # <200 → 明显蓝海
        "medium": 1,   # 200-500
        "low": 0,      # >500 → 红海
    },
    # TOP10卖家数（不含自营）
    "seller_count": {
        "high": 2,     # <10家 → 蓝海
        "medium": 1,   # 10-20家
        "low": 0,      # >20家 → 红海
    },
    # 自营占比
    "ozon_self_ratio": {
        "high": 1,     # 自营占比<10% → 机会大
        "medium": 0.5, # 10-30%
        "low": 0,      # >30% → 自营主导，难竞争
    },
    # 价格集中度（价格标准差/均价，越小越集中）
    "price_concentration": {
        "high": 2,     # >0.4 → 价格分散，有差异化空间
        "medium": 1,   # 0.2-0.4
        "low": 0,      # <0.2 → 价格战激烈
    },
    # 评分分散度
    "rating_variance": {
        "high": 1,     # 差评>20% → 有痛点可解决（差异化机会）
        "medium": 0.5, # 10-20%
        "low": 0,      # <10% → 市场满意度高，差异化空间小
    },
    # rFBS物流适配度（从品类标签推算）
    "rFBS_fitness": {
        "high": 1,     # 轻小件+非液体+非带电
        "medium": 0.5, # 中等体积或需要简单认证
        "low": 0,      # 大件/液体/需EAC认证
    },
}

# ============================================================
# 蓝海评分门槛
# ============================================================
BLUE_OCEAN_THRESHOLD = {
    "strong_recommend": 7,   # ≥7分 → 强烈推荐入场
    "conditional": 5,        # 5-6分 → 有条件入场（需差异化）
    "avoid": 4,              # ≤4分 → 直接放弃
}

# ============================================================
# 告警配置
# ============================================================
ALERT_CONFIG = {
    # 新蓝海出现：上次评分<5，本次评分≥7
    "new_blue_ocean": True,
    # 蓝海变红海：上次评分≥7，本次评分<5
    "blue_to_red": True,
    # 评论数暴增：TOP10平均评论数比上次增长>30%
    "review_explosion": True,
    # 自营介入：上次自营占比<10%，本次>30%
    "ozon_self_entry": True,
    # 价格战加剧：价格集中度从>0.4降到<0.2
    "price_war": True,
}

# ============================================================
# 爬取配置
# ============================================================
SCRAPER_CONFIG = {
    # 每个关键词爬取的搜索结果页数
    "max_pages": 3,
    # 每页商品数（Ozon默认约36个）
    "items_per_page": 36,
    # 爬取间隔（秒）— 避免触发反爬
    "page_delay": 5,
    # 关键词间隔（秒）
    "keyword_delay": 10,
    # 浏览器超时（秒）
    "timeout": 30,
    # 使用headless模式
    "headless": True,
    # 是否启用stealth插件
    "use_stealth": True,
}

# ============================================================
# 数据存储配置
# ============================================================
DATA_CONFIG = {
    # 最新数据文件路径
    "latest_file": "data/latest.json",
    # 历史数据目录
    "history_dir": "data/history",
    # 仪表盘数据文件（供Web Dashboard读取）
    "dashboard_file": "dashboard/data.json",
    # 历史数据保留天数
    "history_retention_days": 90,
}

# ============================================================
# 调度配置（用于Windows任务计划程序或手动运行）
# ============================================================
SCHEDULE_CONFIG = {
    # 建议运行频率
    "recommended_frequency": "daily",
    # 建议运行时间（莫斯科时间对应北京时间）
    "recommended_time_beijing": "06:00",  # 莫斯科01:00，流量低谷期
    # 单次运行预估耗时（分钟）
    "estimated_duration_minutes": 15,
}
