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

# Fix emoji printing on Windows (GBK console can't encode emoji)
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Crash log path on Android
CRASH_LOG = '/data/data/com.bilisummary.bilisummary/files/crash.log'


def log_crash(msg):
    """Write crash info to a file on device for debugging."""
    try:
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(CRASH_LOG, 'a', encoding='utf-8') as f:
            f.write(f'[{ts}] {msg}\n')
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

try:
    from server import app as fastapi_app
    import uvicorn

    def start_server():
        try:
            uvicorn.run(fastapi_app, host="127.0.0.1", port=18520, log_level="warning")
        except Exception as e:
            log_crash(f'Server error: {e}\n{traceback.format_exc()}')

    # Start FastAPI in background thread
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    time.sleep(2.0)
    log_crash('Server thread started, waiting for Kivy...')

except Exception as e:
    log_crash(f'Server import/start error: {e}\n{traceback.format_exc()}')
    raise


try:
    from kivy.app import App
    from kivy.utils import platform
    from kivy.logger import Logger

    class BiliSummaryApp(App):
        def build(self):
            from kivy.uix.widget import Widget
            log_crash('Kivy build() called')
            return Widget()

        def on_start(self):
            log_crash(f'Kivy on_start() called, platform={platform}')
            if platform == 'android':
                try:
                    self._setup_android_webview()
                except Exception as e:
                    log_crash(f'WebView setup error: {e}\n{traceback.format_exc()}')
                    raise
            else:
                import webbrowser
                webbrowser.open('http://127.0.0.1:18520')
                Logger.info("BiliSummary: http://127.0.0.1:18520")

        def _setup_android_webview(self):
            log_crash('Setting up Android WebView...')
            from jnius import autoclass, cast

            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            log_crash(f'Got activity: {activity}')

            # Ensure WebView is created on the UI thread
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            WebSettings = autoclass('android.webkit.WebSettings')

            # Run WebView setup on the UI thread for Android 14+ compatibility
            def create_webview():
                log_crash('Creating WebView on UI thread...')
                webview = WebView(activity)

                settings = webview.getSettings()
                settings.setJavaScriptEnabled(True)
                settings.setDomStorageEnabled(True)
                settings.setAllowFileAccess(True)
                settings.setAllowFileAccessFromFileURLs(True)
                settings.setAllowUniversalAccessFromFileURLs(True)
                settings.setMixedContentMode(
                    autoclass('android.webkit.WebSettings').MIXED_CONTENT_ALWAYS_ALLOW
                )
                # Android 14+ WebView requires these for local network access
                settings.setBlockNetworkLoads(False)
                settings.setBlockNetworkImage(False)

                webview.setWebViewClient(WebViewClient())
                webview.loadUrl('http://127.0.0.1:18520')
                log_crash('WebView created, loading URL...')

                activity.setContentView(webview)
                log_crash('setContentView done')

            try:
                # Try running on UI thread first (required on some Android 14 devices)
                activity.runOnUiThread(create_webview)
            except Exception as e:
                log_crash(f'runOnUiThread failed: {e}, trying direct...')
                create_webview()

    if __name__ == '__main__':
        log_crash('Starting BiliSummaryApp...')
        BiliSummaryApp().run()

except ImportError as e:
    log_crash(f'Kivy import error: {e}')
    # Kivy not installed (desktop dev without Android SDK)
    import webbrowser
    webbrowser.open('http://127.0.0.1:18520')
    Logger.info("BiliSummary: http://127.0.0.1:18520")
    Logger.info("(Kivy not installed, using browser)")

except Exception as e:
    log_crash(f'Fatal error: {e}\n{traceback.format_exc()}')
    raise
