# Ozon蓝海监控系统 — 线上部署指南

三种部署方案，从零成本到付费，按你的情况选择。

---

## 方案一：GitHub Actions + GitHub Pages（✅ 推荐，完全免费）

**原理**：GitHub免费提供CI/CD服务，每天自动运行Python爬取脚本→生成数据→部署Dashboard到GitHub Pages。

### 步骤1：创建GitHub仓库

```bash
# 1. 在GitHub上创建新仓库（如 ozon-blue-ocean-monitor）
# 2. 将项目代码推送到仓库

cd ozon-blue-ocean-monitor
git init
git add .
git commit -m "初始化Ozon蓝海监控系统"
git remote add origin https://github.com/{你的用户名}/ozon-blue-ocean-monitor.git
git push -u origin main
```

### 步骤2：启用GitHub Pages

1. 进入仓库 → Settings → Pages
2. Source 选择 `gh-pages` 分支
3. 等待部署完成（约1-2分钟）
4. 访问地址：`https://{你的用户名}.github.io/ozon-blue-ocean-monitor/`

### 步骤3：验证GitHub Actions

1. 进入仓库 → Actions → Ozon蓝海监控每日运行
2. 点击 **Run workflow** 手动触发一次测试
3. 查看运行日志，确认爬取和分析成功
4. 检查 `dashboard/data.json` 是否已更新

### 步骤4：配置Dashboard远程数据源

在GitHub Pages上的Dashboard页面中：

1. 在"远程数据源"输入框填入：
   ```
   https://raw.githubusercontent.com/{你的用户名}/ozon-blue-ocean-monitor/main/dashboard/data.json
   ```
2. 点击"连接"按钮
3. 数据源自动保存到localStorage，下次访问无需重新配置

### 自动运行时间

- 每天北京时间14:00（莫斯科时间09:00）自动运行
- 也可手动触发（仓库 → Actions → Run workflow）
- 如需修改时间，编辑 `.github/workflows/monitor.yml` 中的 cron 表达式

### 零成本确认

| 项目 | 费用 |
|------|------|
| GitHub 仓库 | 免费（公开仓库） |
| GitHub Actions | 免费（每月2000分钟，单次运行约15分钟） |
| GitHub Pages | 免费 |
| **总计** | **¥0** |

---

## 方案二：本地运行 + CloudStudio Dashboard（最简单）

**原理**：Python脚本在你的电脑上定时运行，Dashboard部署在CloudStudio上，手动上传数据。

### 步骤1：安装Python环境

```bash
# 安装依赖
pip install playwright
playwright install chromium
pip install -r requirements.txt
```

### 步骤2：首次运行测试

```bash
cd ozon-blue-ocean-monitor
python run.py --demo    # 先用演示数据测试Dashboard
python run.py           # 正式爬取Ozon数据
```

### 步骤3：设置Windows定时任务

```powershell
# 创建每天06:00运行的任务
schtasks /create /tn "Ozon蓝海监控" /tr "python C:\path\to\ozon-blue-ocean-monitor\run.py" /sc daily /st 06:00
```

或者用GUI设置：
1. Win+R → `taskschd.msc`
2. 创建基本任务 → 名称"Ozon蓝海监控"
3. 触发器：每天 06:00
4. 操作：启动程序 → `python` → 参数 `run.py` → 起始于 `C:\path\to\ozon-blue-ocean-monitor`

### 步骤4：Dashboard保持在线

Dashboard已部署在CloudStudio上，每次本地运行完`run.py`后，`dashboard/data.json`会自动更新。

**如果需要把最新数据推送到线上Dashboard**：
- 方法A：每次运行后手动在Dashboard页面"从文件加载"导入新的data.json
- 方法B：写一个简单脚本自动上传（需要CloudStudio API）

---

## 方案三：云服务器部署（¥30-50/月）

**原理**：租一台便宜的VPS，全自动化运行，7×24小时不间断。

### 推荐VPS选择

| 供应商 | 价格 | 配置 | 适合 |
|--------|------|------|------|
| 腾讯云轻量 | ¥34/月 | 2核2G | 入门够用 |
| 阿里云ECS | ¥36/月 | 2核2G | 入门够用 |
| Vultr | $6/月 | 1核1G | 海外机房 |

### 部署步骤

```bash
# 1. SSH登录服务器
ssh root@your-server-ip

# 2. 安装Python + Playwright
apt update && apt install -y python3 python3-pip
pip3 install playwright
playwright install chromium --with-deps

# 3. 克隆代码
git clone https://github.com/{你的用户名}/ozon-blue-ocean-monitor.git
cd ozon-blue-ocean-monitor

# 4. 安装依赖
pip3 install -r requirements.txt

# 5. 设置cron定时任务（每天06:00莫斯科01:00）
crontab -e
# 添加这行：
0 6 * * * cd /root/ozon-blue-ocean-monitor && python3 run.py >> /var/log/ozon-monitor.log 2>&1

# 6. 首次运行
python3 run.py --demo
python3 run.py

# 7. 配置Nginx反向代理Dashboard
apt install -y nginx
# 配置 /etc/nginx/sites-available/default
# root /root/ozon-blue-ocean-monitor/dashboard;
# 重启 nginx
systemctl restart nginx
```

---

## 方案对比总结

| 维度 | GitHub Actions | 本地+CloudStudio | 云服务器 |
|------|---------------|-----------------|---------|
| **费用** | ¥0 | ¥0 | ¥30-50/月 |
| **自动化程度** | 全自动 | 半自动（需开机） | 全自动 |
| **稳定性** | 高（GitHub保障） | 中（依赖电脑开机） | 高 |
| **难度** | 中等（需学GitHub） | 低 | 中等 |
| **7×24运行** | ✅ | ❌ | ✅ |
| **推荐** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

---

## 我的建议

**失业起步阶段，选方案一（GitHub Actions）**：
- 完全免费，零风险
- 不依赖你电脑是否开机
- 数据自动保存在GitHub，不会丢失
- Dashboard通过GitHub Pages永久在线

等你有了稳定收入，再考虑方案三升级到云服务器。

---

## 常见问题

**Q: GitHub Actions运行失败怎么办？**
A: 进入仓库 → Actions → 查看失败日志。常见原因：
- Ozon反爬导致超时 → 增大config.py中的timeout
- Chromium安装失败 → 检查workflow中playwright install步骤
- 数据格式异常 → 检查monitor.py输出

**Q: Ozon会不会封我的IP？**
A: GitHub Actions每次运行使用不同IP，且config.py中已设置5秒/page+10秒/keyword的延迟，风险很低。如仍被封，可在workflow中添加代理配置。

**Q: 能否增加监控频率到每小时？**
A: 可以。修改workflow中的cron表达式：
```yaml
schedule:
  - cron: '0 */6 * * *'  # 每6小时
  - cron: '0 0 * * *'    # 每天0点
```
但频率越高，被Ozon反爬的风险越大。建议每天1次即可。

**Q: 数据可以导出Excel吗？**
A: 在Dashboard中点击"从文件加载"导入data.json后，可以用浏览器扩展导出为CSV，或用Python脚本转换：
```python
import json, csv
data = json.load(open('dashboard/data.json'))
with open('export.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['category', 'total_score', 'recommendation', ...])
    writer.writeheader()
    for r in data['ranking']:
        writer.writerow(r)
```
