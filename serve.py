#!/usr/bin/env python3
"""
Ozon蓝海选品Dashboard — 本地服务器
一键启动，自动打开浏览器，告别GitHub Pages等待
"""
import http.server
import socketserver
import webbrowser
import os
import sys
import json
from pathlib import Path
from datetime import datetime

# ========== 配置 ==========
PORT = 8080
ROOT = Path(__file__).parent.resolve()
# ===========================


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    """自定义handler：支持CORS + JSON MIME类型 + 静态文件"""

    def end_headers(self):
        # 允许本地跨域（fetch JSON文件需要）
        self.send_header("Access-Control-Allow-Origin", "*")
        # 禁用缓存，确保每次刷新都拿到最新数据
        if self.path.endswith(".json"):
            self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def guess_type(self, path):
        """确保JSON文件返回正确的MIME类型"""
        if path.endswith(".json"):
            return "application/json; charset=utf-8"
        return super().guess_type(path)

    def log_message(self, format, *args):
        """简洁的日志输出"""
        status = args[1] if len(args) > 1 else "?"
        # 只打印非200状态码
        if "200" not in str(status) and "304" not in str(status):
            print(f"  [{self.log_date_time_string()}] {status} {self.path}")


def check_data_files():
    """检查关键数据文件是否存在"""
    files = [
        ("index.html", "Dashboard主页面"),
        ("dashboard/data.json", "蓝海监控数据"),
        ("daily-picks/latest-picks.json", "选品日报数据"),
    ]
    print("\n  数据文件检查：")
    all_ok = True
    for filepath, desc in files:
        full_path = ROOT / filepath
        if full_path.exists():
            size = full_path.stat().st_size
            print(f"    [OK] {filepath} ({size:,} bytes) — {desc}")
        else:
            print(f"    [!!] {filepath} 不存在 — {desc}")
            all_ok = False
    return all_ok


def print_banner(port, data_ok):
    """打印启动横幅"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "数据完整" if data_ok else "部分数据缺失"
    print("""
  ╔══════════════════════════════════════════════════╗
  ║                                                  ║
  ║   Ozon 蓝海选品 Dashboard — 本地服务器           ║
  ║                                                  ║
  ╚══════════════════════════════════════════════════╝
""")
    print(f"  启动时间 : {now}")
    print(f"  访问地址 : http://localhost:{port}")
    print(f"  数据状态 : {status}")
    print(f"  项目目录 : {ROOT}")
    print()
    print("  操作说明：")
    print("    - 浏览器已自动打开 Dashboard")
    print("    - 按 Ctrl+C 停止服务器")
    print("    - 数据更新后刷新浏览器即可看到最新内容")
    print()


def main():
    # 切换到项目根目录
    os.chdir(ROOT)

    # 检查数据文件
    data_ok = check_data_files()

    # 尝试启动服务器
    try:
        with socketserver.TCPServer(("", PORT), DashboardHandler) as httpd:
            httpd.allow_reuse_address = True
            print_banner(PORT, data_ok)

            # 自动打开浏览器
            url = f"http://localhost:{PORT}"
            try:
                webbrowser.open(url)
                print(f"  浏览器已打开 → {url}")
            except Exception:
                print(f"  请手动打开浏览器访问 → {url}")

            print("\n  服务器运行中...\n")

            # 开始服务
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n\n  服务器已停止。再见！\n")
        sys.exit(0)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"\n  端口 {PORT} 已被占用！")
            print(f"  可能是上一次的服务器还在运行。")
            print(f"  选项1：直接访问 http://localhost:{PORT}")
            print(f"  选项2：杀掉占用进程后重试")
            # 尝试打开浏览器
            webbrowser.open(f"http://localhost:{PORT}")
        else:
            print(f"\n  启动失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
