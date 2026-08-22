/**
 * Ozon蓝海监控仪表盘 — 前端逻辑
 */

// ============================================================
// 演示数据（离线模式）
// ============================================================
const DEMO_DATA = {
    "timestamp": "2026-07-02T22:00:00",
    "ranking": [
        {
            "category": "园艺/达恰工具",
            "keyword_ru": "садовые ножницы",
            "keyword_en": "pruning shears",
            "tags": ["蓝海", "旺季7-9月", "轻小件"],
            "total_score": 8,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 45.2,
            "dimensions": {
                "search_volume": 2, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 2, "rating_variance": 1, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 320, "avg_price": 590, "avg_reviews": 45,
                "avg_rating": 4.6, "unique_sellers": 7, "ozon_self_ratio": 0.03,
                "price_concentration": 0.52, "low_rating_ratio": 0.22,
                "top10_avg_reviews": 38, "top10_avg_rating": 4.5, "top10_seller_count": 6,
                "top10_ozon_self_count": 0, "price_min": 180, "price_max": 1890,
                "price_distribution": {
                    "≤300₽": {"count": 5, "ratio": 0.08},
                    "300-500₽": {"count": 12, "ratio": 0.20},
                    "500-1000₽": {"count": 25, "ratio": 0.42},
                    "1000-1500₽": {"count": 10, "ratio": 0.17},
                    "≥1500₽": {"count": 8, "ratio": 0.13}
                }
            }
        },
        {
            "category": "达恰迷你园艺工具",
            "keyword_ru": "набор инструментов для сада мини",
            "keyword_en": "mini garden tools set",
            "tags": ["蓝海", "旺季4-9月", "轻小件"],
            "total_score": 8,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 38.7,
            "dimensions": {
                "search_volume": 1, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 2, "rating_variance": 1, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 155, "avg_price": 470, "avg_reviews": 28,
                "avg_rating": 4.5, "unique_sellers": 4, "ozon_self_ratio": 0.02,
                "price_concentration": 0.48, "low_rating_ratio": 0.18,
                "top10_avg_reviews": 22, "top10_avg_rating": 4.4, "top10_seller_count": 4,
                "top10_ozon_self_count": 0, "price_min": 220, "price_max": 1200,
                "price_distribution": {
                    "≤300₽": {"count": 3, "ratio": 0.06},
                    "300-500₽": {"count": 15, "ratio": 0.30},
                    "500-1000₽": {"count": 20, "ratio": 0.40},
                    "1000-1500₽": {"count": 7, "ratio": 0.14},
                    "≥1500₽": {"count": 5, "ratio": 0.10}
                }
            }
        },
        {
            "category": "宠物智能用品-猫",
            "keyword_ru": "автоматическая кормушка для кошек",
            "keyword_en": "automatic cat feeder",
            "tags": ["蓝海", "全年品", "轻小件"],
            "total_score": 8,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 52.3,
            "dimensions": {
                "search_volume": 2, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 1, "rating_variance": 1, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 420, "avg_price": 980, "avg_reviews": 62,
                "avg_rating": 4.4, "unique_sellers": 8, "ozon_self_ratio": 0.04,
                "price_concentration": 0.35, "low_rating_ratio": 0.20,
                "top10_avg_reviews": 55, "top10_avg_rating": 4.3, "top10_seller_count": 7,
                "top10_ozon_self_count": 0, "price_min": 350, "price_max": 2500,
                "price_distribution": {
                    "≤300₽": {"count": 2, "ratio": 0.03},
                    "300-500₽": {"count": 5, "ratio": 0.08},
                    "500-1000₽": {"count": 18, "ratio": 0.30},
                    "1000-1500₽": {"count": 15, "ratio": 0.25},
                    "≥1500₽": {"count": 20, "ratio": 0.34}
                }
            }
        },
        {
            "category": "车载冬季应急",
            "keyword_ru": "автоодеяло с подогревом",
            "keyword_en": "car heated blanket",
            "tags": ["蓝海", "旺季10-2月", "需备货"],
            "total_score": 8,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 41.8,
            "dimensions": {
                "search_volume": 2, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 2, "rating_variance": 0.5, "rFBS_fitness": 0.5
            },
            "metrics": {
                "total_search_results": 280, "avg_price": 1650, "avg_reviews": 38,
                "avg_rating": 4.7, "unique_sellers": 6, "ozon_self_ratio": 0.02,
                "price_concentration": 0.55, "low_rating_ratio": 0.08,
                "top10_avg_reviews": 30, "top10_avg_rating": 4.6, "top10_seller_count": 5,
                "top10_ozon_self_count": 0, "price_min": 500, "price_max": 4200,
                "price_distribution": {
                    "≤300₽": {"count": 0, "ratio": 0},
                    "300-500₽": {"count": 3, "ratio": 0.05},
                    "500-1000₽": {"count": 8, "ratio": 0.13},
                    "1000-1500₽": {"count": 20, "ratio": 0.33},
                    "≥1500₽": {"count": 29, "ratio": 0.49}
                }
            }
        },
        {
            "category": "达恰用品",
            "keyword_ru": "инструменты для дачи",
            "keyword_en": "dacha tools",
            "tags": ["蓝海", "旺季5-8月", "轻小件"],
            "total_score": 7,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 32.5,
            "dimensions": {
                "search_volume": 1, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 2, "rating_variance": 0, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 195, "avg_price": 720, "avg_reviews": 35,
                "avg_rating": 4.8, "unique_sellers": 5, "ozon_self_ratio": 0.05,
                "price_concentration": 0.45, "low_rating_ratio": 0.05,
                "top10_avg_reviews": 28, "top10_avg_rating": 4.7, "top10_seller_count": 5,
                "top10_ozon_self_count": 0, "price_min": 250, "price_max": 2100,
                "price_distribution": {
                    "≤300₽": {"count": 4, "ratio": 0.07},
                    "300-500₽": {"count": 10, "ratio": 0.17},
                    "500-1000₽": {"count": 22, "ratio": 0.37},
                    "1000-1500₽": {"count": 12, "ratio": 0.20},
                    "≥1500₽": {"count": 12, "ratio": 0.20}
                }
            }
        },
        {
            "category": "俄语书法/教育用品",
            "keyword_ru": "набор для каллиграфии",
            "keyword_en": "calligraphy set",
            "tags": ["政策红利", "新需求", "轻小件"],
            "total_score": 7,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 28.9,
            "dimensions": {
                "search_volume": 1, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 1, "rating_variance": 1, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 75, "avg_price": 990, "avg_reviews": 18,
                "avg_rating": 4.5, "unique_sellers": 3, "ozon_self_ratio": 0,
                "price_concentration": 0.38, "low_rating_ratio": 0.25,
                "top10_avg_reviews": 12, "top10_avg_rating": 4.3, "top10_seller_count": 3,
                "top10_ozon_self_count": 0, "price_min": 450, "price_max": 1800,
                "price_distribution": {
                    "≤300₽": {"count": 0, "ratio": 0},
                    "300-500₽": {"count": 3, "ratio": 0.10},
                    "500-1000₽": {"count": 12, "ratio": 0.40},
                    "1000-1500₽": {"count": 10, "ratio": 0.33},
                    "≥1500₽": {"count": 5, "ratio": 0.17}
                }
            }
        },
        {
            "category": "家居收纳-冰箱收纳",
            "keyword_ru": "органайзер для холодильника",
            "keyword_en": "fridge organizer",
            "tags": ["刚需", "全年品", "轻小件"],
            "total_score": 7,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 35.2,
            "dimensions": {
                "search_volume": 2, "avg_reviews": 1, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 1, "rating_variance": 0, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 380, "avg_reviews": 220,
                "avg_rating": 4.6, "unique_sellers": 10, "ozon_self_ratio": 0.08,
                "price_concentration": 0.28, "low_rating_ratio": 0.10,
                "top10_avg_reviews": 180, "top10_avg_rating": 4.5, "top10_seller_count": 8,
                "top10_ozon_self_count": 1, "price_min": 150, "price_max": 800,
                "avg_price": 420,
                "price_distribution": {
                    "≤300₽": {"count": 8, "ratio": 0.13},
                    "300-500₽": {"count": 20, "ratio": 0.33},
                    "500-1000₽": {"count": 18, "ratio": 0.30},
                    "1000-1500₽": {"count": 5, "ratio": 0.08},
                    "≥1500₽": {"count": 9, "ratio": 0.16}
                }
            }
        },
        {
            "category": "厨房小工具-调料瓶",
            "keyword_ru": "контейнеры для специй",
            "keyword_en": "spice containers",
            "tags": ["刚需", "全年品", "轻小件"],
            "total_score": 7,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 30.1,
            "dimensions": {
                "search_volume": 1, "avg_reviews": 1, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 1, "rating_variance": 0.5, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 180, "avg_price": 380, "avg_reviews": 150,
                "avg_rating": 4.5, "unique_sellers": 6, "ozon_self_ratio": 0.05,
                "price_concentration": 0.32, "low_rating_ratio": 0.12,
                "top10_avg_reviews": 120, "top10_avg_rating": 4.4, "top10_seller_count": 5,
                "top10_ozon_self_count": 0, "price_min": 180, "price_max": 950,
                "price_distribution": {
                    "≤300₽": {"count": 10, "ratio": 0.17},
                    "300-500₽": {"count": 22, "ratio": 0.37},
                    "500-1000₽": {"count": 18, "ratio": 0.30},
                    "1000-1500₽": {"count": 5, "ratio": 0.08},
                    "≥1500₽": {"count": 5, "ratio": 0.08}
                }
            }
        },
        {
            "category": "车载配件-手机支架",
            "keyword_ru": "держатель для телефона в авто с зарядкой",
            "keyword_en": "car phone holder wireless charging",
            "tags": ["蓝海", "全年品", "轻小件"],
            "total_score": 7,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 25.6,
            "dimensions": {
                "search_volume": 2, "avg_reviews": 1, "seller_count": 1,
                "ozon_self": 1, "price_concentration": 1, "rating_variance": 0.5, "rFBS_fitness": 0.5
            },
            "metrics": {
                "total_search_results": 520, "avg_price": 680, "avg_reviews": 280,
                "avg_rating": 4.3, "unique_sellers": 12, "ozon_self_ratio": 0.06,
                "price_concentration": 0.30, "low_rating_ratio": 0.15,
                "top10_avg_reviews": 250, "top10_avg_rating": 4.2, "top10_seller_count": 10,
                "top10_ozon_self_count": 1, "price_min": 250, "price_max": 1800,
                "price_distribution": {
                    "≤300₽": {"count": 5, "ratio": 0.08},
                    "300-500₽": {"count": 15, "ratio": 0.23},
                    "500-1000₽": {"count": 25, "ratio": 0.40},
                    "1000-1500₽": {"count": 10, "ratio": 0.16},
                    "≥1500₽": {"count": 5, "ratio": 0.13}
                }
            }
        },
        {
            "category": "宠物智能用品-小型犬",
            "keyword_ru": "автокормушка для собак малых пород",
            "keyword_en": "small dog automatic feeder",
            "tags": ["蓝海", "全年品", "轻小件"],
            "total_score": 7,
            "recommendation": "🔥 强烈推荐入场",
            "blue_ocean_index": 22.3,
            "dimensions": {
                "search_volume": 1, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 1, "rating_variance": 0, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 120, "avg_price": 1200, "avg_reviews": 32,
                "avg_rating": 4.6, "unique_sellers": 5, "ozon_self_ratio": 0.03,
                "price_concentration": 0.35, "low_rating_ratio": 0.08,
                "top10_avg_reviews": 25, "top10_avg_rating": 4.5, "top10_seller_count": 5,
                "top10_ozon_self_count": 0, "price_min": 500, "price_max": 2800,
                "price_distribution": {
                    "≤300₽": {"count": 0, "ratio": 0},
                    "300-500₽": {"count": 3, "ratio": 0.05},
                    "500-1000₽": {"count": 15, "ratio": 0.25},
                    "1000-1500₽": {"count": 20, "ratio": 0.33},
                    "≥1500₽": {"count": 22, "ratio": 0.37}
                }
            }
        },
        {
            "category": "宠物玩具-互动类",
            "keyword_ru": "игрушка для кошек интерактивная",
            "keyword_en": "interactive cat toy",
            "tags": ["探索", "复购率高", "轻小件"],
            "total_score": 6,
            "recommendation": "🌊 有条件入场（需差异化）",
            "blue_ocean_index": 18.5,
            "dimensions": {
                "search_volume": 1, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 0, "rating_variance": 0, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 85, "avg_price": 350, "avg_reviews": 15,
                "avg_rating": 4.4, "unique_sellers": 4, "ozon_self_ratio": 0.02,
                "price_concentration": 0.18, "low_rating_ratio": 0.08,
                "top10_avg_reviews": 10, "top10_avg_rating": 4.3, "top10_seller_count": 3,
                "top10_ozon_self_count": 0, "price_min": 120, "price_max": 800,
                "price_distribution": {
                    "≤300₽": {"count": 12, "ratio": 0.28},
                    "300-500₽": {"count": 15, "ratio": 0.35},
                    "500-1000₽": {"count": 10, "ratio": 0.23},
                    "1000-1500₽": {"count": 3, "ratio": 0.07},
                    "≥1500₽": {"count": 3, "ratio": 0.07}
                }
            }
        },
        {
            "category": "冬季保暖-暖手宝",
            "keyword_ru": "портативный обогреватель для рук",
            "keyword_en": "portable hand warmer",
            "tags": ["探索", "旺季10-2月", "轻小件"],
            "total_score": 6,
            "recommendation": "🌊 有条件入场（需差异化）",
            "blue_ocean_index": 15.3,
            "dimensions": {
                "search_volume": 1, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 0, "rating_variance": 0, "rFBS_fitness": 1
            },
            "metrics": {
                "total_search_results": 65, "avg_price": 450, "avg_reviews": 12,
                "avg_rating": 4.5, "unique_sellers": 4, "ozon_self_ratio": 0,
                "price_concentration": 0.15, "low_rating_ratio": 0.06,
                "top10_avg_reviews": 8, "top10_avg_rating": 4.4, "top10_seller_count": 3,
                "top10_ozon_self_count": 0, "price_min": 200, "price_max": 900,
                "price_distribution": {
                    "≤300₽": {"count": 5, "ratio": 0.20},
                    "300-500₽": {"count": 10, "ratio": 0.40},
                    "500-1000₽": {"count": 8, "ratio": 0.32},
                    "1000-1500₽": {"count": 2, "ratio": 0.08},
                    "≥1500₽": {"count": 0, "ratio": 0}
                }
            }
        },
        {
            "category": "冬季保暖-加热手套",
            "keyword_ru": "перчатки с подогревом USB",
            "keyword_en": "USB heated gloves",
            "tags": ["探索", "旺季10-2月", "轻小件"],
            "total_score": 5,
            "recommendation": "🌊 有条件入场（需差异化）",
            "blue_ocean_index": 12.7,
            "dimensions": {
                "search_volume": 0, "avg_reviews": 2, "seller_count": 2,
                "ozon_self": 1, "price_concentration": 0, "rating_variance": 0, "rFBS_fitness": 0.5
            },
            "metrics": {
                "total_search_results": 28, "avg_price": 520, "avg_reviews": 8,
                "avg_rating": 4.3, "unique_sellers": 3, "ozon_self_ratio": 0,
                "price_concentration": 0.12, "low_rating_ratio": 0.10,
                "top10_avg_reviews": 5, "top10_avg_rating": 4.2, "top10_seller_count": 2,
                "top10_ozon_self_count": 0, "price_min": 280, "price_max": 1100,
                "price_distribution": {
                    "≤300₽": {"count": 2, "ratio": 0.15},
                    "300-500₽": {"count": 5, "ratio": 0.38},
                    "500-1000₽": {"count": 6, "ratio": 0.46},
                    "1000-1500₽": {"count": 0, "ratio": 0},
                    "≥1500₽": {"count": 0, "ratio": 0}
                }
            }
        },
        {
            "category": "厨房收纳-折叠置物架",
            "keyword_ru": "складная полка для кухни",
            "keyword_en": "foldable kitchen shelf",
            "tags": ["刚需", "全年品", "中等体积"],
            "total_score": 5,
            "recommendation": "🌊 有条件入场（需差异化）",
            "blue_ocean_index": 14.2,
            "dimensions": {
                "search_volume": 1, "avg_reviews": 1, "seller_count": 1,
                "ozon_self": 1, "price_concentration": 1, "rating_variance": 0, "rFBS_fitness": 0.5
            },
            "metrics": {
                "total_search_results": 220, "avg_price": 680, "avg_reviews": 350,
                "avg_rating": 4.5, "unique_sellers": 15, "ozon_self_ratio": 0.06,
                "price_concentration": 0.25, "low_rating_ratio": 0.08,
                "top10_avg_reviews": 280, "top10_avg_rating": 4.4, "top10_seller_count": 12,
                "top10_ozon_self_count": 1, "price_min": 300, "price_max": 2200,
                "price_distribution": {
                    "≤300₽": {"count": 3, "ratio": 0.05},
                    "300-500₽": {"count": 8, "ratio": 0.13},
                    "500-1000₽": {"count": 25, "ratio": 0.42},
                    "1000-1500₽": {"count": 12, "ratio": 0.20},
                    "≥1500₽": {"count": 12, "ratio": 0.20}
                }
            }
        },
        {
            "category": "3C配件-手机壳（红海对照）",
            "keyword_ru": "чехол для телефона",
            "keyword_en": "phone case",
            "tags": ["红海对照", "超饱和", "不入场"],
            "total_score": 2,
            "recommendation": "❌ 建议放弃",
            "blue_ocean_index": 3.2,
            "dimensions": {
                "search_volume": 2, "avg_reviews": 0, "seller_count": 0,
                "ozon_self": 0, "price_concentration": 0, "rating_variance": 0, "rFBS_fitness": 0
            },
            "metrics": {
                "total_search_results": 12000, "avg_price": 290, "avg_reviews": 1500,
                "avg_rating": 4.3, "unique_sellers": 85, "ozon_self_ratio": 0.20,
                "price_concentration": 0.08, "low_rating_ratio": 0.10,
                "top10_avg_reviews": 1200, "top10_avg_rating": 4.5, "top10_seller_count": 25,
                "top10_ozon_self_count": 4, "price_min": 80, "price_max": 1500,
                "price_distribution": {
                    "≤300₽": {"count": 40, "ratio": 0.55},
                    "300-500₽": {"count": 20, "ratio": 0.28},
                    "500-1000₽": {"count": 8, "ratio": 0.11},
                    "1000-1500₽": {"count": 3, "ratio": 0.04},
                    "≥1500₽": {"count": 1, "ratio": 0.02}
                }
            }
        },
        {
            "category": "宠物保暖衣（红海对照）",
            "keyword_ru": "зимняя одежда для собак",
            "keyword_en": "winter dog clothes",
            "tags": ["红海对照", "退货率高", "不入场"],
            "total_score": 3,
            "recommendation": "❌ 建议放弃",
            "blue_ocean_index": 5.8,
            "dimensions": {
                "search_volume": 2, "avg_reviews": 0, "seller_count": 0,
                "ozon_self": 0, "price_concentration": 0, "rating_variance": 1, "rFBS_fitness": 0
            },
            "metrics": {
                "total_search_results": 5000, "avg_price": 450, "avg_reviews": 800,
                "avg_rating": 3.8, "unique_sellers": 45, "ozon_self_ratio": 0.18,
                "price_concentration": 0.10, "low_rating_ratio": 0.30,
                "top10_avg_reviews": 600, "top10_avg_rating": 3.9, "top10_seller_count": 20,
                "top10_ozon_self_count": 3, "price_min": 200, "price_max": 2800,
                "price_distribution": {
                    "≤300₽": {"count": 15, "ratio": 0.20},
                    "300-500₽": {"count": 25, "ratio": 0.33},
                    "500-1000₽": {"count": 18, "ratio": 0.24},
                    "1000-1500₽": {"count": 8, "ratio": 0.11},
                    "≥1500₽": {"count": 9, "ratio": 0.12}
                }
            }
        }
    ],
    "alerts": [
        {
            "type": "🟢 新蓝海发现",
            "category": "俄语书法/教育用品",
            "message": "「俄语书法/教育用品」蓝海评分7分，政策红利驱动，强烈推荐入场！",
            "priority": "high"
        },
        {
            "type": "⚠️ 评论暴增",
            "category": "家居收纳-冰箱收纳",
            "message": "「家居收纳-冰箱收纳」TOP10评论从120增长到180（+50%），竞争正在加剧",
            "priority": "medium"
        }
    ],
    "summary": {
        "total_categories": 16,
        "strong_recommend": 10,
        "conditional": 4,
        "avoid": 2,
        "avg_score": 6.5
    }
};

// ============================================================
// 全局状态
// ============================================================
let currentData = null;
let selectedCategory = null;
let scoreChart = null;
let priceChart = null;
let competitionChart = null;

// ============================================================
// 数据加载
// ============================================================

// 远程数据URL配置（部署到GitHub后修改为你的仓库地址）
// 格式: https://raw.githubusercontent.com/{用户名}/{仓库名}/main/dashboard/data.json
let REMOTE_DATA_URL = '';  // 空字符串=使用本地DEMO数据

function loadDemoData() {
    currentData = DEMO_DATA;
    renderDashboard(currentData);
    document.getElementById('data-badge').className = 'badge badge-demo';
    document.getElementById('data-badge').textContent = 'DEMO';
}

function loadRemoteData() {
    if (!REMOTE_DATA_URL) {
        console.log('未配置远程数据URL，使用DEMO数据');
        loadDemoData();
        return;
    }
    console.log('正在加载远程数据:', REMOTE_DATA_URL);
    fetch(REMOTE_DATA_URL)
        .then(res => {
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return res.json();
        })
        .then(data => {
            currentData = data;
            renderDashboard(currentData);
            document.getElementById('data-badge').className = 'badge badge-live';
            document.getElementById('data-badge').textContent = 'LIVE';
            console.log('远程数据加载成功');
        })
        .catch(err => {
            console.warn('远程数据加载失败，使用DEMO数据:', err);
            loadDemoData();
        });
}

function setRemoteUrl(url) {
    REMOTE_DATA_URL = url;
    localStorage.setItem('ozon_remote_url', url);
    loadRemoteData();
}

function loadImportedData() {
    const input = document.getElementById('data-input').value.trim();
    if (!input) {
        alert('请先粘贴JSON数据');
        return;
    }
    try {
        const data = JSON.parse(input);
        currentData = data;
        renderDashboard(currentData);
        document.getElementById('data-badge').className = 'badge badge-live';
        document.getElementById('data-badge').textContent = 'LIVE';
    } catch (e) {
        alert('JSON格式错误: ' + e.message);
    }
}

function loadFromFile() {
    // 创建文件选择器
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.json';
    input.onchange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (ev) => {
            try {
                const data = JSON.parse(ev.target.result);
                currentData = data;
                renderDashboard(currentData);
                document.getElementById('data-badge').className = 'badge badge-live';
                document.getElementById('data-badge').textContent = 'LIVE';
            } catch (err) {
                alert('JSON格式错误: ' + err.message);
            }
        };
        reader.readAsText(file);
    };
    input.click();
}

function applyRemoteUrl() {
    const url = document.getElementById('remote-url').value.trim();
    if (!url) {
        alert('请输入远程数据URL');
        return;
    }
    setRemoteUrl(url);
}

function clearRemoteUrl() {
    REMOTE_DATA_URL = '';
    localStorage.removeItem('ozon_remote_url');
    document.getElementById('remote-url').value = '';
    loadDemoData();
}

// ============================================================
// Dashboard渲染
// ============================================================
function renderDashboard(data) {
    // 更新时间
    const ts = data.timestamp || data.date || '-';
    document.getElementById('update-time').textContent = `更新: ${ts}`;

    // 统计概览
    const summary = data.summary || {};
    document.getElementById('stat-strong').textContent = summary.strong_recommend || '-';
    document.getElementById('stat-conditional').textContent = summary.conditional || '-';
    document.getElementById('stat-avoid').textContent = summary.avoid || '-';
    document.getElementById('stat-avg').textContent = summary.avg_score || '-';

    // 告警
    renderAlerts(data.alerts || []);

    // 排行榜
    renderRanking(data.ranking || []);

    // 图表
    renderScoreChart(data.ranking || []);
    renderPriceChart(data.ranking || []);
    renderCompetitionChart(data.ranking || []);
}

// ============================================================
// 告警渲染
// ============================================================
function renderAlerts(alerts) {
    const bar = document.getElementById('alerts-bar');
    if (!alerts.length) {
        bar.innerHTML = '';
        return;
    }
    bar.innerHTML = alerts.map(a => `
        <div class="alert-item alert-${a.priority === 'high' ? 'high' : a.priority === 'medium' ? 'medium' : 'low'}">
            <span style="font-size:16px;">${a.type}</span>
            <span>${a.message}</span>
        </div>
    `).join('');
}

// ============================================================
// 排行榜渲染
// ============================================================
function renderRanking(ranking) {
    const list = document.getElementById('ranking-list');
    list.innerHTML = ranking.map((r, i) => {
        const rankClass = i === 0 ? 'rank-1' : i === 1 ? 'rank-2' : i === 2 ? 'rank-3' : 'rank-default';
        const fillClass = r.total_score >= 7 ? 'fill-high' : r.total_score >= 5 ? 'fill-medium' : 'fill-low';
        const scoreColor = r.total_score >= 7 ? '#ef4444' : r.total_score >= 5 ? '#3b82f6' : '#64748b';
        const tagsHtml = (r.tags || []).map(t => {
            const cls = t.includes('蓝海') ? 'tag-blue-ocean' :
                        t.includes('红海') ? 'tag-red-ocean' :
                        t.includes('旺季') || t.includes('季节') ? 'tag-season' :
                        t.includes('轻小') ? 'tag-light' :
                        t.includes('政策') ? 'tag-policy' :
                        'tag-explore';
            return `<span class="tag ${cls}">${t}</span>`;
        }).join('');

        return `
            <li class="ranking-item" onclick="selectCategory(${i})" data-index="${i}">
                <span class="rank ${rankClass}">${i + 1}</span>
                <div class="info">
                    <div class="cat-name">${r.category}</div>
                    <div class="cat-tags">${tagsHtml}</div>
                </div>
                <div class="score-bar">
                    <div class="bar"><div class="fill ${fillClass}" style="width:${r.total_score * 10}%"></div></div>
                    <span class="num" style="color:${scoreColor}">${r.total_score}</span>
                </div>
            </li>
        `;
    }).join('');
}

// ============================================================
// 品类详情
// ============================================================
function selectCategory(index) {
    // 高亮选中
    document.querySelectorAll('.ranking-item').forEach(el => el.classList.remove('selected'));
    document.querySelector(`.ranking-item[data-index="${index}"]`).classList.add('selected');

    selectedCategory = currentData.ranking[index];
    renderDetail(selectedCategory);
}

function renderDetail(cat) {
    const panel = document.getElementById('detail-panel');
    panel.style.display = 'block';

    document.getElementById('detail-title').textContent = `${cat.category} — 详细分析`;

    // 核心指标卡片
    const m = cat.metrics;
    const grid = document.getElementById('detail-grid');
    grid.innerHTML = `
        <div class="detail-metric">
            <div class="dm-label">蓝海指数</div>
            <div class="dm-value" style="color:var(--accent-cyan)">${cat.blue_ocean_index}</div>
            <div class="dm-unit">搜索结果/卖家数</div>
        </div>
        <div class="detail-metric">
            <div class="dm-label">平均售价</div>
            <div class="dm-value">${m.avg_price}<span class="dm-unit">₽</span></div>
            <div class="dm-unit">${m.price_min}-${m.price_max}₽</div>
        </div>
        <div class="detail-metric">
            <div class="dm-label">TOP10平均评论</div>
            <div class="dm-value">${m.top10_avg_reviews}</div>
            <div class="dm-unit">条</div>
        </div>
        <div class="detail-metric">
            <div class="dm-label">TOP10卖家数</div>
            <div class="dm-value">${m.top10_seller_count}</div>
            <div class="dm-unit">家</div>
        </div>
        <div class="detail-metric">
            <div class="dm-label">自营占比</div>
            <div class="dm-value">${(m.ozon_self_ratio * 100).toFixed(1)}<span class="dm-unit">%</span></div>
            <div class="dm-unit">${m.top10_ozon_self_count}个自营商品</div>
        </div>
        <div class="detail-metric">
            <div class="dm-label">价格集中度</div>
            <div class="dm-value">${m.price_concentration.toFixed(2)}</div>
            <div class="dm-unit">越高=差异化空间越大</div>
        </div>
        <div class="detail-metric">
            <div class="dm-label">低评分占比</div>
            <div class="dm-value">${(m.low_rating_ratio * 100).toFixed(1)}<span class="dm-unit">%</span></div>
            <div class="dm-unit">越高=痛点越多=差异化机会</div>
        </div>
        <div class="detail-metric">
            <div class="dm-label">搜索结果数</div>
            <div class="dm-value">${m.total_search_results}</div>
            <div class="dm-unit">个商品</div>
        </div>
    `;

    // 评分维度表格
    const dims = cat.dimensions || {};
    const dimLabels = {
        "search_volume": { name: "搜索需求量", criteria: "≥100=2分, 30-100=1分, <30=0分" },
        "avg_reviews": { name: "TOP10平均评论", criteria: "<200=2分, 200-500=1分, >500=0分" },
        "seller_count": { name: "TOP10卖家数", criteria: "<10=2分, 10-20=1分, >20=0分" },
        "ozon_self": { name: "自营占比", criteria: "<10%=1分, 10-30%=0.5分, >30%=0分" },
        "price_concentration": { name: "价格集中度", criteria: ">0.4=2分, 0.2-0.4=1分, <0.2=0分" },
        "rating_variance": { name: "低评分占比", criteria: ">20%=1分, 10-20%=0.5分, <10%=0分" },
        "rFBS_fitness": { name: "rFBS物流适配", criteria: "轻小件=1分, 中等=0.5分, 大件/EAC=0分" },
    };

    const dimDetails = {
        "search_volume": `搜索结果${m.total_search_results}个`,
        "avg_reviews": `TOP10平均${m.top10_avg_reviews}条评论`,
        "seller_count": `TOP10有${m.top10_seller_count}家卖家`,
        "ozon_self": `自营占比${(m.ozon_self_ratio * 100).toFixed(1)}%`,
        "price_concentration": `价格集中度${m.price_concentration.toFixed(2)}`,
        "rating_variance": `低评分占比${(m.low_rating_ratio * 100).toFixed(1)}%`,
        "rFBS_fitness": `标签: ${(cat.tags || []).join(', ')}`,
    };

    const tbody = document.getElementById('dimension-tbody');
    tbody.innerHTML = Object.keys(dimLabels).map(key => {
        const score = dims[key] || 0;
        const cls = score >= 2 ? 'dim-2' : score >= 1 ? 'dim-1' : score >= 0.5 ? 'dim-05' : 'dim-0';
        return `
            <tr>
                <td><strong>${dimLabels[key].name}</strong></td>
                <td><span class="dim-score ${cls}">${score}</span></td>
                <td>${dimDetails[key] || '-'}</td>
                <td style="color:var(--text-muted);font-size:12px">${dimLabels[key].criteria}</td>
            </tr>
        `;
    }).join('');
}

// ============================================================
// 图表渲染
// ============================================================
function renderScoreChart(ranking) {
    const ctx = document.getElementById('score-chart').getContext('2d');
    if (scoreChart) scoreChart.destroy();

    const labels = ranking.map(r => r.category.length > 10 ? r.category.substring(0, 10) + '...' : r.category);
    const scores = ranking.map(r => r.total_score);
    const colors = scores.map(s => s >= 7 ? '#ef4444' : s >= 5 ? '#3b82f6' : '#64748b');

    scoreChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: '蓝海评分',
                data: scores,
                backgroundColor: colors.map(c => c + '40'),
                borderColor: colors,
                borderWidth: 2,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        title: (items) => ranking[items[0].dataIndex]?.category || '',
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 10,
                    grid: { color: '#334155' },
                    ticks: { color: '#94a3b8' },
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8', maxRotation: 45 },
                }
            }
        }
    });
}

function renderPriceChart(ranking) {
    const ctx = document.getElementById('price-chart').getContext('2d');
    if (priceChart) priceChart.destroy();

    // 只取蓝海品类（评分≥5）
    const blueCats = ranking.filter(r => r.total_score >= 5);
    const labels = ['≤300₽', '300-500₽', '500-1000₽', '1000-1500₽', '≥1500₽'];

    const datasets = blueCats.slice(0, 6).map((r, i) => {
        const dist = r.metrics?.price_distribution || {};
        const hue = [200, 160, 280, 30, 340, 120][i];
        return {
            label: r.category.length > 12 ? r.category.substring(0, 12) + '...' : r.category,
            data: labels.map(l => (dist[l]?.ratio || 0) * 100),
            backgroundColor: `hsla(${hue}, 70%, 60%, 0.3)`,
            borderColor: `hsla(${hue}, 70%, 60%, 1)`,
            borderWidth: 2,
            borderRadius: 2,
        };
    });

    priceChart = new Chart(ctx, {
        type: 'bar',
        data: { labels, datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', boxWidth: 12, font: { size: 11 } }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 60,
                    grid: { color: '#334155' },
                    ticks: { color: '#94a3b8', callback: v => v + '%' },
                    title: { display: true, text: '占比%', color: '#94a3b8' },
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#94a3b8' },
                }
            }
        }
    });
}

function renderCompetitionChart(ranking) {
    const ctx = document.getElementById('competition-chart').getContext('2d');
    if (competitionChart) competitionChart.destroy();

    const blueCats = ranking.filter(r => r.total_score >= 5).slice(0, 8);
    const labels = blueCats.map(r => r.category.length > 8 ? r.category.substring(0, 8) + '...' : r.category);

    competitionChart = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['蓝海指数', '评论少', '卖家少', '自营低', '价格散', '差评多'],
            datasets: blueCats.map((r, i) => {
                const m = r.metrics;
                // 标准化到0-10
                const boi = Math.min(r.blue_ocean_index / 60 * 10, 10);
                const reviewScore = Math.max(10 - m.top10_avg_reviews / 200 * 10, 0);
                const sellerScore = Math.max(10 - m.top10_seller_count / 20 * 10, 0);
                const selfScore = Math.max(10 - m.ozon_self_ratio * 100 / 30 * 10, 0);
                const priceScore = Math.min(m.price_concentration / 0.6 * 10, 10);
                const ratingScore = Math.min(m.low_rating_ratio * 100 / 30 * 10, 10);

                const hue = [200, 160, 280, 30, 340, 120, 60, 100][i];
                return {
                    label: r.category.length > 10 ? r.category.substring(0, 10) + '..' : r.category,
                    data: [boi, reviewScore, sellerScore, selfScore, priceScore, ratingScore],
                    backgroundColor: `hsla(${hue}, 70%, 60%, 0.15)`,
                    borderColor: `hsla(${hue}, 70%, 60%, 0.8)`,
                    borderWidth: 2,
                    pointRadius: 3,
                    pointBackgroundColor: `hsla(${hue}, 70%, 60%, 1)`,
                };
            })
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#94a3b8', boxWidth: 10, font: { size: 10 } }
                }
            },
            scales: {
                r: {
                    beginAtZero: true,
                    max: 10,
                    grid: { color: '#334155' },
                    angleLines: { color: '#334155' },
                    pointLabels: { color: '#94a3b8', font: { size: 11 } },
                    ticks: { display: false },
                }
            }
        }
    });
}

// ============================================================
// 初始化
// ============================================================
document.addEventListener('DOMContentLoaded', () => {
    // 检查是否配置了远程数据URL
    const savedUrl = localStorage.getItem('ozon_remote_url');
    if (savedUrl) {
        REMOTE_DATA_URL = savedUrl;
        document.getElementById('remote-url').value = savedUrl;
    }

    // 尝试加载远程数据，失败则使用DEMO数据
    loadRemoteData();
});
