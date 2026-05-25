#!/usr/bin/env python3
"""
BiliSummary Android 入口
Kivy 壳 + 本地 FastAPI 服务 + WebView
桌面端可用于测试（打开浏览器访问 localhost:18520）
"""

import os
import sys
import threading
import time

# Fix emoji printing on Windows (GBK console can't encode emoji)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass


def get_bundle_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def get_data_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    try:
        from android.storage import app_storage_path
        return app_storage_path()
    except ImportError:
        return os.path.dirname(os.path.abspath(__file__))


os.environ['BILISUMMARY_BUNDLE_DIR'] = get_bundle_dir()
os.environ['BILISUMMARY_DATA_DIR'] = get_data_dir()

from server import app as fastapi_app
import uvicorn


def start_server():
    uvicorn.run(fastapi_app, host="127.0.0.1", port=18520, log_level="warning")


# Start FastAPI in background thread
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(1.5)

try:
    from kivy.app import App
    from kivy.utils import platform

    class BiliSummaryApp(App):
        def build(self):
            from kivy.uix.widget import Widget
            return Widget()

        def on_start(self):
            if platform == 'android':
                self._setup_android_webview()
            else:
                import webbrowser
                webbrowser.open('http://127.0.0.1:18520')
                print("BiliSummary 服务已启动: http://127.0.0.1:18520")

        def _setup_android_webview(self):
            from jnius import autoclass

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity

            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            WebSettings = autoclass('android.webkit.WebSettings')

            webview = WebView(activity)

            settings = webview.getSettings()
            settings.setJavaScriptEnabled(True)
            settings.setDomStorageEnabled(True)
            settings.setAllowFileAccess(True)
            settings.setMixedContentMode(
                autoclass('android.webkit.WebSettings').MIXED_CONTENT_ALWAYS_ALLOW
            )

            webview.setWebViewClient(WebViewClient())
            webview.loadUrl('http://127.0.0.1:18520')

            activity.setContentView(webview)

    if __name__ == '__main__':
        BiliSummaryApp().run()

except ImportError:
    # Kivy not installed (desktop dev without Android SDK)
    import webbrowser
    webbrowser.open('http://127.0.0.1:18520')
    print("BiliSummary 服务已启动: http://127.0.0.1:18520")
    print("(Kivy 未安装，使用浏览器访问。Android 打包请安装 kivy)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("已退出")
