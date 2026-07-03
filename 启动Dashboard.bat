@echo off
chcp 65001 >nul 2>&1
title Ozon蓝海选品Dashboard — 本地服务器
echo.
echo  正在启动 Ozon 蓝海选品 Dashboard...
echo.
python serve.py
pause
