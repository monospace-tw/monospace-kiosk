# Monospace 門口與入口看板

GitHub Actions 在 main 更新時發布 GitHub Pages。根目錄是門口版，scripts/build_board.py 另產生 boards/reception-1107/ 入口版。請把字型、圖形和 QR Code 內嵌於同一個 HTML，以便設備離線播放。

2026-11-08 顯示「雙手牌工作室｜今日課程」，依 Asia/Taipei 日期於 11/9 00:00 自動回到一般迎賓內容。日期判斷在本機執行，離線、跨日與重新開機也適用。每台保留自己的服務區與 LINE QR，不含已結束活動的報名、人數或時間。Pi 原有面板保護提供每 90 秒構圖輪替與微位移。

頁首圖標來自 https://monospace.tw/images/logo.png ，已內嵌供離線播放。WelcomeTC 是 Noto Sans CJK TC Bold 的文字子集，授權附於 HTML 與 FONT-LICENSE.txt。既有 BrandDM 字標沿用原素材。

請保留 head 裡的 application-name 標記（Monospace Kiosk），檔案要小於或等於 2 MiB。Pages 發布後，門口機約每三分鐘透過 HTTPS 檢查新版，並保存最近成功播放的頁面供重新上電使用。
