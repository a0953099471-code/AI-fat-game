# AI 燃脂闖關遊戲

這個專案是一個使用 Python、Flask、OpenCV 與 MediaPipe 建立的「燃脂闖關遊戲」。透過攝影機自動偵測你的動作，將運動轉成遊戲操作，並展示玩家資訊、Boss 血量、卡路里與分數。

## 功能

- 深蹲 → 攻擊
- 開合跳 → 集氣
- 抬腿 → 閃避
- 平板撐 → 防禦
- 自動即時偵測動作，不需按快門鍵
- 顯示玩家血量、Boss 血量、卡路里、分數
- 連續追蹤遊戲進度與每日紀錄

## 技術架構

- Python 物件導向設計 (`game.py`)
- Flask 網頁介面 + HTML/CSS (`app.py`, `templates/index.html`, `static/style.css`)
- OpenCV 攝影機串流與影像處理 (`tracker.py`)
- MediaPipe 姿勢偵測
- Pandas 資料紀錄與視覺化基礎

## 安裝與執行

1. 進入專案目錄：

```bash
cd /workspaces/0913
```

2. 建議建立虛擬環境：

```bash
python3 -m venv venv
source venv/bin/activate
```

3. 安裝相依套件：

```bash
pip install -r requirements.txt
```

4. 執行 Flask 應用程式（現有版本）：

```bash
python3 app.py
```

5. 若要使用 Streamlit 網頁版本，請安裝套件後執行：

```bash
streamlit run streamlit_app.py
```

6. 開啟瀏覽器，訪問 Streamlit 所提供的本機連結（通常是 `http://localhost:8501`）。

7. 進入頁面後，瀏覽器會要求使用攝影機權限，請允許後即可啟動相機，自動開始偵測動作。

## 部署為永久網址

要讓這個應用 "永遠可訪問"，請使用雲端部署平台，例如 Streamlit Community Cloud。步驟如下：

1. 將專案推送到 GitHub：

```bash
git add .
git commit -m "Add Streamlit app and deployment config"
git push origin main
```

2. 登入 Streamlit Community Cloud：https://share.streamlit.io
3. 連結你的 GitHub 帳號，選擇 `peggypig950913/0913` repository
4. 設定入口檔為 `streamlit_app.py`
5. 部署後即可得到永久公開網址，例如 `https://your-app-name.streamlit.app`

若不想使用 Streamlit Cloud，也可以選擇 Render、Railway、Heroku、Google Cloud Run、Azure App Service 等平台，啟動命令同樣是：

```bash
streamlit run streamlit_app.py
```

## 使用說明

- 允許瀏覽器使用攝影機。
- 進入頁面後，鏡頭會自動啟動並持續偵測動作。
- 畫面左側顯示玩家狀態與即時鏡頭串流。
- 右側顯示 Boss 血量、卡路里、分數與最新紀錄。

## 注意

- 目前動作偵測為簡單範例，若偵測準確度不足，可調整 `tracker.py` 的判斷條件。
- 若遇到相機權限或無法開啟問題，請確認系統相機設備可用。python app.py