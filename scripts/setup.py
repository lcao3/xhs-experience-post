#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键安装依赖：python3 setup.py 即可（Windows 双击 setup.bat 也行）"""
import subprocess, sys

def run(cmd):
    print(">>", cmd)
    subprocess.check_call(cmd, shell=True)

print("== 安装 Python 依赖 ==")
run(f"{sys.executable} -m pip install --upgrade pip")
run(f"{sys.executable} -m pip install playwright")

print("== 检查/安装 Chromium 浏览器 ==")
import shutil
need = True
for name in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "chrome", "msedge"):
    if shutil.which(name):
        print(f"检测到系统浏览器：{name}，跳过下载")
        need = False
        break
if need:
    run(f"{sys.executable} -m playwright install chromium")

print("\n完成！现在可以：")
print("  1. 修改 build.py 里的内容（你的干货文字）")
print("  2. 运行 python3 build.py 生成页面")
print("  3. 运行 python3 render_all.py 输出高清 PNG 图片")
