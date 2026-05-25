package com.bilisummary;

import android.app.Activity;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.chaquo.python.Python;
import com.chaquo.python.android.AndroidPlatform;

public class MainActivity extends Activity {
    private static final String URL = "http://127.0.0.1:18520";
    private WebView webView;
    private TextView loadingText;
    private Handler handler;
    private int pollCount = 0;
    private static final int MAX_POLLS = 60; // ~30 seconds

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Create layout: WebView (hidden) + Loading text
        FrameLayout layout = new FrameLayout(this);
        FrameLayout.LayoutParams matchParent = new FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.MATCH_PARENT,
            FrameLayout.LayoutParams.MATCH_PARENT
        );

        // Loading overlay
        loadingText = new TextView(this);
        loadingText.setText("Loading...");
        loadingText.setTextSize(18);
        loadingText.setTextColor(0xFFCCCCCC);
        FrameLayout.LayoutParams textParams = new FrameLayout.LayoutParams(
            FrameLayout.LayoutParams.WRAP_CONTENT,
            FrameLayout.LayoutParams.WRAP_CONTENT
        );
        textParams.gravity = android.view.Gravity.CENTER;
        loadingText.setLayoutParams(textParams);

        // WebView
        webView = new WebView(this);
        webView.setLayoutParams(matchParent);
        webView.setVisibility(View.GONE);

        setupWebView();

        layout.addView(webView);
        layout.addView(loadingText);
        setContentView(layout);

        handler = new Handler(Looper.getMainLooper());
        startPython();
    }

    private void setupWebView() {
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageFinished(WebView view, String url) {
                webView.setVisibility(View.VISIBLE);
                loadingText.setVisibility(View.GONE);
            }

            @Override
            public void onReceivedError(WebView view, int errorCode, String description, String failingUrl) {
                loadingText.setText("Error: " + description);
            }
        });
    }

    private void startPython() {
        new Thread(() -> {
            try {
                if (!Python.isStarted()) {
                    Python.start(new AndroidPlatform(this));
                }

                // Wait for server to be ready, then load URL
                pollServer();
            } catch (Exception e) {
                runOnUiThread(() -> {
                    loadingText.setText("Startup failed:\n" + e.getMessage());
                    Toast.makeText(this, "Failed: " + e.getMessage(), Toast.LENGTH_LONG).show();
                });
            }
        }).start();
    }

    private void pollServer() {
        if (pollCount++ >= MAX_POLLS) {
            runOnUiThread(() -> {
                loadingText.setText("Server timed out.\nTap to retry.");
                loadingText.setOnClickListener(v -> {
                    pollCount = 0;
                    loadingText.setText("Loading...");
                    startPython();
                });
            });
            return;
        }

        try {
            java.net.URL url = new java.net.URL(URL + "/api/status");
            java.net.HttpURLConnection conn = (java.net.HttpURLConnection) url.openConnection();
            conn.setConnectTimeout(2000);
            conn.setReadTimeout(2000);
            int code = conn.getResponseCode();
            conn.disconnect();

            if (code == 200) {
                runOnUiThread(() -> webView.loadUrl(URL));
                return;
            }
        } catch (Exception ignored) {
            // Server not ready yet
        }

        handler.postDelayed(this::pollServer, 500);
    }
}
