@echo off
chcp 65001 >nul
echo 正在为你安装依赖，请稍等（第一次会下载浏览器，约1-2分钟）...
python setup.py
pause
