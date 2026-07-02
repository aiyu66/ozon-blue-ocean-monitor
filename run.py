"""
Ozon蓝海自动监控系统 — 一键运行脚本
自动执行: monitor.py → analyzer.py → 更新Dashboard数据
"""

import subprocess
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


def run_step(script_name, description):
    """运行一个Python脚本"""
    script_path = PROJECT_ROOT / script_name
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=str(PROJECT_ROOT),
        capture_output=False,
    )

    if result.returncode != 0:
        print(f"❌ {description} 失败 (退出码: {result.returncode})")
        return False

    print(f"✅ {description} 完成")
    return True


def main():
    """一键运行完整监控流程"""
    print("\n" + "=" * 60)
    print("🚀 Ozon蓝海自动监控 — 一键运行")
    print("=" * 60)

    # 检查命令行参数
    demo_mode = "--demo" in sys.argv

    if demo_mode:
        # Step 1: 生成演示数据
        if not run_step("monitor.py", "生成演示数据"):
            return

        # Step 2: 运行分析
        if not run_step("analyzer.py", "蓝海评分分析"):
            return
    else:
        # Step 1: 爬取Ozon实时数据
        if not run_step("monitor.py", "爬取Ozon品类数据"):
            return

        # Step 2: 运行分析
        if not run_step("analyzer.py", "蓝海评分分析"):
            return

    print("\n" + "=" * 60)
    print("✅ 全流程完成！Dashboard数据已更新")
    print(f"   数据文件: {PROJECT_ROOT / 'dashboard' / 'data.json'}")
    print(f"   打开: {PROJECT_ROOT / 'dashboard' / 'index.html'}")
    print("=" * 60)


if __name__ == "__main__":
    main()
