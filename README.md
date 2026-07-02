# Ozon蓝海自动监控系统

> 自动监控Ozon品类竞争数据，计算蓝海评分，发现蓝海机会，预警红海风险

## 📁 项目结构

```
ozon-blue-ocean-monitor/
├── .github/workflows/
│   └── monitor.yml    # GitHub Actions自动化定时任务
├── config.py          # 配置文件（关键词、评分阈值、调度参数）
├── monitor.py         # 主爬取脚本（Playwright + Ozon搜索页）
├── analyzer.py        # 蓝海分析引擎（评分 + 告警）
├── run.py             # 一键运行脚本
├── dashboard/
│   ├── index.html     # 可视化仪表盘（支持远程数据源）
│   ├── app.js         # 仪表盘前端逻辑
│   └── data.json      # 仪表盘数据（自动生成）
├── data/
│   ├── latest.json    # 最新爬取数据
│   ├── history/       # 历史数据（按日期保存）
│   └── analysis_history/  # 分析结果历史
├── requirements.txt   # Python依赖
├── DEPLOY-GUIDE.md    # 线上部署指南（GitHub Actions/本地/云服务器）
└── README.md          # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Linux/Mac

# 安装Python依赖
pip install playwright

# 安装Playwright浏览器
playwright install chromium
```

### 2. 生成演示数据（离线模式）

不想爬取Ozon？先用演示数据看看效果：

```bash
python run.py --demo
```

然后打开 `dashboard/index.html` 查看仪表盘。

### 3. 爬取实时数据（在线模式）

```bash
python run.py
```

> ⚠️ 首次运行会启动Playwright浏览器爬取Ozon搜索页，每个关键词约需30-60秒。全部关键词约需15分钟。

### 4. 单独运行

```bash
# 只爬取数据
python monitor.py

# 只生成演示数据
python monitor.py --demo

# 只运行分析
python analyzer.py
```

## 📊 Dashboard使用

打开 `dashboard/index.html`，有四种导入数据的方式：

1. **远程数据源** — 配置GitHub仓库URL，自动加载最新监控数据（部署后启用）
2. **加载演示数据** — 点击按钮，内置模拟数据立即查看
3. **粘贴JSON** — 将 `data/data.json` 或 `dashboard/data.json` 的内容粘贴到文本框
4. **从文件加载** — 选择本地的JSON文件导入

Dashboard功能：
- 🏆 蓝海品类排行榜（按7维度评分排序）
- 📊 评分分布柱状图
- 💰 价格区间分布对比图
- 📈 TOP10竞争指标雷达图
- 🔔 告警通知（新蓝海/蓝海变红海/评论暴增/自营介入/价格战）
- 📋 品类详情（点击排行榜中任意品类查看7维度评分明细）

## ⏰ 设置定时监控（Windows任务计划程序）

### 方法一：PowerShell脚本

创建 `schedule_run.ps1`：

```powershell
# 每天北京时间06:00运行（莫斯科01:00，流量低谷）
cd "C:\path\to\ozon-blue-ocean-monitor"
python run.py
```

然后在Windows任务计划程序中：
1. 创建基本任务 → 名称："Ozon蓝海监控"
2. 触发器：每天 06:00
3. 操作：启动程序 → `powershell.exe` → 参数：`-File "C:\path\to\schedule_run.ps1"`

### 方法二：直接命令

在任务计划程序中：
1. 创建基本任务
2. 触发器：每天 06:00
3. 操作：启动程序
   - 程序：`C:\path\to\venv\Scripts\python.exe`
   - 参数：`C:\path\to\ozon-blue-ocean-monitor\run.py`
   - 起始于：`C:\path\to\ozon-blue-ocean-monitor`

## 🔧 配置自定义关键词

编辑 `config.py` 中的 `MONITOR_KEYWORDS` 列表：

```python
{
    "keyword_ru": "你的俄语关键词",       # Ozon搜索用俄语
    "keyword_en": "你的英语关键词",       # 对照参考
    "category": "品类名称",               # Dashboard显示名
    "tags": ["标签1", "标签2"],           # 影响rFBS评分维度
}
```

## 📐 蓝海评分体系（满分10分）

| 维度 | 满分 | 判断标准 |
|------|------|----------|
| 搜索需求量 | 2 | 搜索结果≥100=2, 30-100=1, <30=0 |
| TOP10平均评论 | 2 | <200=2(蓝海), 200-500=1, >500=0(红海) |
| TOP10卖家数 | 2 | <10=2(蓝海), 10-20=1, >20=0(红海) |
| 自营占比 | 1 | <10%=1, 10-30%=0.5, >30%=0 |
| 价格集中度 | 2 | >0.4=2(差异化空间大), 0.2-0.4=1, <0.2=0(价格战) |
| 低评分占比 | 1 | >20%=1(痛点=机会), 10-20%=0.5, <10%=0 |
| rFBS物流适配 | 1 | 轻小件=1, 中等=0.5, 大件/EAC=0 |

**评分结论**：
- ≥7分 → 🔥 强烈推荐入场
- 5-6分 → 🌊 有条件入场（需差异化）
- ≤4分 → ❌ 建议放弃

## ⚠️ 注意事项

1. **反爬风险**：脚本已加入随机延迟和反检测脚本，但仍可能被Ozon检测。建议：
   - 每天只运行1次
   - 运行时间选择流量低谷（莫斯科01:00=北京06:00）
   - 关键词数量控制在20个以内

2. **数据准确性**：Ozon页面结构可能变化，导致爬取失败。遇到问题时：
   - 检查Playwright版本是否最新
   - 查看 `data/latest.json` 中是否有空数据
   - 调整 `config.py` 中的CSS选择器

3. **演示数据**：首次使用建议先运行 `--demo` 模式，确认Dashboard正常后再爬取真实数据

## 🌐 线上部署

详见 **[DEPLOY-GUIDE.md](DEPLOY-GUIDE.md)**，提供三种方案：

| 方案 | 费用 | 推荐度 |
|------|------|--------|
| GitHub Actions + GitHub Pages | ¥0 | ⭐⭐⭐⭐⭐ |
| 本地运行 + CloudStudio Dashboard | ¥0 | ⭐⭐⭐ |
| 云服务器（VPS） | ¥30-50/月 | ⭐⭐ |

**推荐方案一（GitHub Actions）**：完全免费，7×24自动运行，数据永久保存在GitHub。
