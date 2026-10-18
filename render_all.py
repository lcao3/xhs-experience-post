#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一键渲染全部页面：把 pages/ 下所有 html 转成高清 PNG。
Windows 双击 render_all.bat，Mac/Linux 运行 python3 render_all.py
"""
import os, subprocess, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))
RENDER = os.path.join(HERE, "scripts", "render.py")

htmls = sorted(glob.glob(os.path.join(HERE, "pages", "*.html")))
if not htmls:
    print("没有找到 pages/*.html，请先运行 build.py 生成页面")
    sys.exit(1)

for h in htmls:
    out = os.path.splitext(h)[0] + ".png"
    print(f"渲染 {os.path.basename(h)} -> {os.path.basename(out)}")
    subprocess.check_call([sys.executable, RENDER, h, out, "1080", "1440", "2"])

print(f"\n完成！共输出 {len(htmls)} 张 2160x2880 高清图，在 pages/ 目录里。")
