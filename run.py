"""
Ozon蓝海自动监控系统 — 一键运行脚本 v2.0
自动执行: data_collector.py → analyzer.py → 更新Dashboard数据

v2.0 变更：用多源数据聚合（data_collector.py）替换Playwright爬虫（monitor.py）
"""

import subprocess
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent


def run_step(script_name, description, extra_args=None):
    """运行一个Python脚本"""
    script_path = PROJECT_ROOT / script_name
    args = [sys.executable, str(script_path)]
    if extra_args:
        args.extend(extra_args)
    
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"{'='*60}")

    result = subprocess.run(
        args,
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
    print("🚀 Ozon蓝海自动监控 v2.0 — 一键运行")
    print("   数据来源: 多源公开数据聚合（替代Playwright爬虫）")
    print("=" * 60)

    # 检查命令行参数
    demo_mode = "--demo" in sys.argv

    if demo_mode:
        print("\n⚠️  demo模式：使用monitor.py的随机演示数据")
        if not run_step("monitor.py", "生成演示数据", extra_args=["--demo"]):
            return
    else:
        # Step 1: 多源数据采集
        if not run_step("data_collector.py", "多源市场数据采集"):
            return

    # Step 2: 蓝海评分分析
    if not run_step("analyzer.py", "蓝海评分分析"):
        return

    # Step 3: 选品数据更新
    print("\n" + "─" * 40)
    print("📊 数据来源汇总:")
    print("   - Ozon官方报告（Q1 2026, Q3 2025）")
    print("   - 星连ERP / 巽迈网络 行业分析")
    print("   - 亿恩网 / 和讯网 / 邦阅网 行业报道")
    print("   - 大数跨境 / 奥维云网 市场研究")
    print("   - 1688 货源数据")
    print("─" * 40)

    print("\n" + "=" * 60)
    print("✅ 全流程完成！Dashboard数据已更新")
    print(f"   数据文件: {PROJECT_ROOT / 'dashboard' / 'data.json'}")
    print(f"   Dashboard: {PROJECT_ROOT / 'index.html'}")
    print(f"   线上地址: https://aiyu66.github.io/ozon-blue-ocean-monitor")
    print("=" * 60)


if __name__ == "__main__":
    main()
