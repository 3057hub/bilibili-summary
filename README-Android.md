# BiliSummary Android 版

Bilibili 视频 AI 总结器 — Android APK，仅消耗个人 DeepSeek API Token。

## 安装

1. 下载 APK 安装到 Android 10+ 设备
2. 首次启动需允许「未知来源」安装（设置 → 安全 → 安装未知应用）

## 配置

1. 打开 App → 底部「设置」Tab
2. API Base URL：`https://api.deepseek.com/anthropic`
3. API Token：填入你的 DeepSeek API Key
4. 默认模型：`deepseek-chat`（或从列表中选择）
5. 点击「保存配置」

## 使用

- **总结**：粘贴 B站视频链接，点击「开始总结」
- **收藏**：点击底部登录按钮扫码 → 选择收藏夹 → 批量总结
- **浏览**：查看所有已生成的总结，支持缩略图和列表视图
- **设置**：配置 API Key、切换模型

## 常见问题

**Q: 语音识别（ASR）不可用？**
A: ASR 默认关闭。如需启用，需自行编译含 PyAV 的 APK 版本并在 config.toml 中开启。

**Q: 扫码登录失败？**
A: 确保 Bilibili App 已登录，且设备和 Android 设备在同一网络下。

**Q: 总结生成慢？**
A: 视频字幕越长处理越久。可在设置中调整模型或减少并发数。

**Q: 需要外网服务器吗？**
A: 不需要。全部在本地设备运行，仅需访问 B站 API 和 DeepSeek API。
