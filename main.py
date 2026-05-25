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
import traceback
import datetime

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

CRASH_LOG = '/data/data/com.bilisummary.bilisummary/files/crash.log'
HEARTBEAT = '/data/data/com.bilisummary.bilisummary/files/heartbeat.txt'


def heartbeat(msg):
    """Write heartbeat to track progress, even if crash happens later."""
    try:
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        with open(HEARTBEAT, 'a', encoding='utf-8') as f:
            f.write(f'[{ts}] {msg}\n')
    except Exception:
        pass


def show_android_error(title, msg):
    """Show an Android AlertDialog with error info - no Kivy needed."""
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        AlertDialog = autoclass('android.app.AlertDialog$Builder')
        dialog = AlertDialog(activity)
        dialog.setTitle(title)
        dialog.setMessage(str(msg)[:2000])
        dialog.setPositiveButton('OK', None)
        dialog.show()
    except Exception:
        pass


heartbeat('=== App started ===')

# Global crash handler
def global_excepthook(exc_type, exc_value, exc_tb):
    tb_text = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    heartbeat(f'FATAL: {tb_text}')
    show_android_error('App Crashed', tb_text)
    sys.__excepthook__(exc_type, exc_value, exc_tb)

sys.excepthook = global_excepthook


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
heartbeat('Paths set')

# --- Import server ---
heartbeat('Importing server...')
try:
    from server import app as fastapi_app
    import uvicorn
    heartbeat('Server imports OK')
except Exception as e:
    heartbeat(f'Server import FAILED: {e}\n{traceback.format_exc()}')
    show_android_error('Import Error', f'Failed to import server:\n{e}')
    raise

# --- Start server thread ---
def start_server():
    try:
        heartbeat('Uvicorn starting...')
        uvicorn.run(fastapi_app, host="127.0.0.1", port=18520, log_level="warning")
    except Exception as e:
        heartbeat(f'Uvicorn error: {e}\n{traceback.format_exc()}')

server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()
time.sleep(2.0)
heartbeat('Server thread started')

# --- Start Kivy ---
heartbeat('Importing Kivy...')
from kivy.app import App
from kivy.utils import platform
from kivy.logger import Logger

heartbeat(f'Kivy imported, platform={platform}')

class BiliSummaryApp(App):
    def build(self):
        heartbeat('build() called')
        from kivy.uix.widget import Widget
        return Widget()

    def on_start(self):
        heartbeat(f'on_start(), platform={platform}')
        if platform == 'android':
            self._setup_android_webview()
        else:
            import webbrowser
            webbrowser.open('http://127.0.0.1:18520')
            Logger.info("BiliSummary: http://127.0.0.1:18520")

    def _setup_android_webview(self):
        heartbeat('WebView setup starting...')
        from jnius import autoclass

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        activity = PythonActivity.mActivity
        heartbeat(f'Got activity OK')

        WebView = autoclass('android.webkit.WebView')
        WebViewClient = autoclass('android.webkit.WebViewClient')
        heartbeat('WebView classes loaded')

        webview = WebView(activity)
        heartbeat('WebView created')

        settings = webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setDomStorageEnabled(True)
        settings.setAllowFileAccess(True)
        settings.setMixedContentMode(
            autoclass('android.webkit.WebSettings').MIXED_CONTENT_ALWAYS_ALLOW
        )
        heartbeat('WebView settings done')

        webview.setWebViewClient(WebViewClient())
        webview.loadUrl('http://127.0.0.1:18520')
        heartbeat('WebView loading URL')

        activity.setContentView(webview)
        heartbeat('setContentView done - WebView should be visible')


if __name__ == '__main__':
    heartbeat('Calling BiliSummaryApp().run()...')
    BiliSummaryApp().run()
