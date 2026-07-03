# GitHub 仓库创建与推送指南

## 问题诊断

你之前的 `error: failed to push some refs` 错误原因有两个：
1. **仓库在 GitHub 上还没创建** — 这是最主要的原因
2. **网络连接被墙** — HTTPS 方式连接 GitHub 在国内不稳定

已解决：
- ✅ SSH 密钥已生成并添加到 `~/.ssh/id_ed25519`
- ✅ SSH config 已配置（使用 ssh.github.com:443 端口绕过防火墙）
- ✅ SSH 认证已验证成功（`Hi aiyu66!`）
- ✅ 远程 URL 已改为 SSH 格式（`git@github.com:aiyu66/ozon-blue-ocean-monitor.git`）

## 操作步骤（请按顺序执行）

### Step 1：在 GitHub 创建仓库

1. 打开浏览器访问 https://github.com/new
2. Repository name 填：`ozon-blue-ocean-monitor`
3. **⚠️ 重要：不要勾选 "Add a README file"**
4. **⚠️ 重要：不要勾选 ".gitignore" 或 "License"**
5. 选择 **Public**（公开仓库，GitHub Pages 需要公开）
6. 点击 **Create repository**

### Step 2：添加 SSH 公钥到 GitHub（如果还没做）

1. 打开 https://github.com/settings/keys
2. 点击 **New SSH key**
3. Title 填：`Ozon-Dev-PC`
4. Key type 选：**Authentication Key**
5. 粘贴以下公钥：

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIKK9NhwFkD83S68L4Wq+2ypBU+fMgLMlbpGTFw2/flNP aiyu66@github
```

6. 点击 **Add SSH key**

### Step 3：推送代码

打开终端（Git Bash 或 PowerShell），执行：

```bash
cd "C:/Users/fangtao/WorkBuddy/2026-07-01-22-14-39/ozon-blue-ocean-monitor"
git push origin master
```

如果推送成功，你会看到类似：
```
Enumerating objects: XX, done.
...
To git@github.com:aiyu66/ozon-blue-ocean-monitor.git
 * [new branch]      master -> master
```

### Step 4：启用 GitHub Pages

1. 打开 https://github.com/aiyu66/ozon-blue-ocean-monitor/settings/pages
2. Source 选择 **Deploy from a branch**
3. Branch 选 **master**，文件夹选 **/ (root)**
4. 点击 **Save**
5. 等待几分钟，Dashboard 就可以通过 `https://aiyu66.github.io/ozon-blue-ocean-monitor/dashboard/` 访问

### Step 5：配置 GitHub Actions 自动运行

GitHub Actions workflow 文件已经在 `.github/workflows/monitor.yml` 中准备好了。

但需要添加一个 **Repository Secret** 来让 Actions 能自动推送数据：

1. 打开 https://github.com/aiyu66/ozon-blue-ocean-monitor/settings/secrets/actions
2. 点击 **New repository secret**
3. Name 填：`ACTIONS_DEPLOY_KEY`
4. Value 填你的 SSH 私钥内容（在终端执行 `cat ~/.ssh/id_ed25519` 查看）
5. 点击 **Add secret**

之后每天北京时间 14:00 GitHub Actions 会自动运行爬取脚本。

---

## 常见问题

### Q: 推送还是报错怎么办？

检查以下几点：
1. 仓库是否已经创建（浏览器访问 https://github.com/aiyu66/ozon-blue-ocean-monitor）
2. SSH 公钥是否已添加（访问 https://github.com/settings/keys 查看列表）
3. 远程 URL 是否是 SSH 格式：`git remote -v` 确认显示 `git@github.com:...`

### Q: 创建仓库时勾选了 README 怎么办？

如果创建仓库时勾选了 README，推送会报冲突错误。解决方法：
```bash
git pull origin master --allow-unrelated-histories
git push origin master
```

### Q: Clash/VPN 配置问题？

SSH 方式已经通过 `ssh.github.com:443` 绕过了防火墙问题，不再需要配置 Git 代理。
但如果浏览器访问 GitHub 也不稳定，确保 Clash for Windows 的 "System Proxy" 模式已开启。
