# Monospace 門口看板

GitHub Pages 由 main 分支的根目錄發布。修改 index.html 並推送到 main 即可更新。請把字型、圖形和 QR Code 內嵌於同一個 HTML，以便門口機離線播放。

上方 QR Code 是活動報名，下方是訪客 LINE。請保持兩者靜止。報名人數由編輯更新 index.html 的 .count 文字，沒有串接 Luma。頁首圖標來自 https://monospace.tw/images/logo.png ，已內嵌供離線播放。

請保留 head 裡的 application-name 標記（Monospace Kiosk），檔案要小於或等於 2 MiB。Pages 發布後，PVE 約每三分鐘檢查並傳送新版。門口機保存最近接收的頁面供重新上電播放。
