# Monospace 門口與入口看板

GitHub Actions 在 main 更新時發布 GitHub Pages。根目錄是門口版，scripts/build_board.py 另產生 boards/reception-1107/ 入口版。請把字型、圖形和 QR Code 內嵌於同一個 HTML，以便設備離線播放。

2026-11-08 顯示「雙手牌工作室｜今日課程」，依 Asia/Taipei 日期於 11/9 00:00 自動回到一般迎賓內容。日期判斷在本機執行，離線、跨日與重新開機也適用。每台保留自己的服務區與 LINE QR，不含已結束活動的報名、人數或時間。Pi 原有面板保護提供每 90 秒構圖輪替與微位移。

頁首圖標來自 https://monospace.tw/images/logo.png ，已內嵌供離線播放。WelcomeTC 是 Noto Sans CJK TC Bold 的文字子集，授權附於 HTML 與 FONT-LICENSE.txt。既有 BrandDM 字標沿用原素材。

請保留 head 裡的 application-name 標記（Monospace Kiosk），檔案要小於或等於 2 MiB。Pages 發布後，門口機約每三分鐘透過 HTTPS 檢查新版，並保存最近成功播放的頁面供重新上電使用。

## 門口平板畫面保護

`assets/door-protection.css` 與 `assets/door-protection.js` 僅由建置器內嵌到門口版；入口版不包含這組設定。仍為單檔離線播放，無新增前端框架。

- 每 180 秒切換暖白圖文、淡綠左右換位、深綠純字版；換版在三分鐘邊界後第 10 秒，九分鐘一輪。
- 深綠版將服務帶移到上方，變換大面積明暗與固定資訊位置；原版忍者使用暖白襯底維持辨識度。
- 每分鐘第 25 秒更換微位移位置，九個整數座標，水平最多 ±6px、垂直最多 ±4px。背景始終滿版，QR 在下一次位移／換版前保持靜止。
- 保留每分鐘第 0 秒的原 Logo 動畫。換版與位移直接套用，不使用全畫面淡入淡出、濾鏡或持續動畫迴圈；不強制建立 GPU 圖層。
- 依本機時間決定版型，重載不會總是回第一張。若替代 Pi 注入 `data-panel-layout`，自動停用此組保護，避免雙重排程。
- 降低長時間固定圖像的暴露，不保證消除殘影；此功能不調整背光或夜間待機。

驗證：`python3 scripts/build_board.py`、`node --test tests/door-protection.test.cjs`。變更後需檢查三個版型的實機截圖、LINE QR、整分鐘特效與負載。未選定的新忍者概念圖不在此次更新範圍。
