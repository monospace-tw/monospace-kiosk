# Monospace 門口看板

GitHub Actions 在 main 更新時發布 GitHub Pages，也排程每 15 分鐘讀取 Luma 公開頁面的 Going 人數並重新發布。若讀取失敗，線上保留上一份成功版本。請把字型、圖形和 QR Code 內嵌於同一個 HTML，以便門口機離線播放。

上方 QR Code 是活動報名，下方是訪客 LINE。請保持兩者靜止。建置時以 Luma 公開的 Going 人數替換 data-luma-going 標記內的預覽數字。頁首圖標來自 https://monospace.tw/images/logo.png ，已內嵌供離線播放。

請保留 head 裡的 application-name 標記（Monospace Kiosk），檔案要小於或等於 2 MiB。Pages 發布後，門口機約每三分鐘透過 HTTPS 檢查新版，並保存最近成功播放的頁面供重新上電使用。
