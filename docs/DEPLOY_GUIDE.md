# ZeroPulse 1.0 - 5 分鐘部署教學

## 快速開始 (本地測試)

### 步驟 1: 安裝依賴
```bash
# 前端無需安裝，直接開啟 HTML

# 後端 (可選)
cd server
npm install
npm start
```

### 步驟 2: 開啟網站
```bash
# 方法 1: 雙擊 website/index.html
# 或用任何 HTTP 伺服器:
python -m http.server 8000
# 然後瀏覽器開啟 http://localhost:8000/website/index.html
```

### 步驟 3: 客戶端測試
```bash
# 安裝 Python 套件
pip install pyautogui psutil

# 執行 GUI
cd client
python gui.py
```

---

## 線上部署 (真實賣)

### 網站部署 - Vercel (免費)

1. **註冊 Vercel**
   - 進入 vercel.com
   - 用 GitHub 帳號登入

2. **部署網站**
   - 新增專案 → 選擇本地資料夾
   - 選 `website/` 資料夾
   - 點「Deploy」→ 自動部署

3. **綁定自訂域名**
   - 在 Namecheap 買 `zeropulse.club` (NT$300/年)
   - Vercel 設定 → 加入自訂域名
   - 更改 DNS 指向 Vercel

### 後端部署 - Railway (免費)

1. **註冊 Railway**
   - 進入 railway.app
   - 用 GitHub 帳號登入

2. **部署 API**
   - 新增專案 → Deploy from GitHub
   - 選擇此倉庫
   - 設定 root directory 為 `server/`
   - 點「Deploy」→ 自動部署

3. **取得 API URL**
   ```
   https://zeropulse-api.railway.app
   ```

### 客戶端 - 打包 EXE

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "ZeroPulse" client/gui.py
# 執行檔在 dist/ZeroPulse.exe
```

---

## 序號管理

### 生成序號格式
```
ZP-M-XXXX-XXXX-XXXX  (月費)
ZP-Q-XXXX-XXXX-XXXX  (季費)
ZP-L-XXXX-XXXX-XXXX  (終身)
```

### 測試序號
- 月費: `ZP-M-TEST-1234`
- 季費: `ZP-Q-TEST-5678`
- 終身: `ZP-L-TEST-9999`

---

## 常見問題

### Q: 能不能修改價格？
**A:** 修改 `website/index.html` 的價格標籤即可

### Q: 怎麼新增新序號？
**A:** 在 `server/index.js` 的 `validSerials` 物件加入:
```javascript
'ZP-M-ABCD-1234': { type: 'month', expiry: '2025-12-31', hwid: null }
```

### Q: 客戶端可以盜版嗎？
**A:** 
- HWID 綁定 (一個序號一台電腦)
- 每 30 秒心跳驗證
- 序號過期自動封鎖

### Q: 私人伺服器用得安全嗎？
**A:** 100% 安全。無 EAC 的私人伺服器沒有風險。

---

## 月收預估

| 方案 | 價格 | 預期客戶/月 | 月收 |
|------|------|-----------|-----|
| 月費 | NT$399 | 30 人 | NT$11,970 |
| 季費 | NT$999 | 10 人 | NT$9,990 |
| 終身 | NT$2999 | 5 人 | NT$14,995 |
| **總計** | - | 45 人 | **NT$36,955/月** |

---

## 售後支援

- Discord 伺服器: https://discord.gg/zeropulse
- 郵件支援: support@zeropulse.club
- 常見問題: https://zeropulse.club/faq

---

祝你賣到爆！ZeroPulse 帝國，正式啟動！ 🚀
