#!/usr/bin/env python3
"""
BiliSummary Chaquopy 入口
仅负责启动 FastAPI 服务器，WebView 由 Java 原生 Activity 处理。
"""

import os
import sys
import threading
import time

# ---- Path setup ----
_base = os.path.dirname(os.path.abspath(__file__))
os.environ['BILISUMMARY_BUNDLE_DIR'] = _base
os.environ['BILISUMMARY_DATA_DIR'] = _base

sys.path.insert(0, _base)

# ---- Start server ----
from server import app as fastapi_app
import uvicorn


def _start():
    uvicorn.run(fastapi_app, host="127.0.0.1", port=18520, log_level="warning")


t = threading.Thread(target=_start, daemon=True)
t.start()
# Block until server is actually listening
time.sleep(2.0)
