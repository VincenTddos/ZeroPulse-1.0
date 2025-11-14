// server.js - ZeroPulse 驗證 API (簡單版)

const express = require('express');
const cors = require('cors');
const app = express();

app.use(express.json());
app.use(cors());

// 簡單的序號資料庫 (實際應該用真實資料庫)
const validSerials = {
    'ZP-M-TEST-1234': { type: 'month', expiry: '2025-12-31', hwid: null },
    'ZP-Q-TEST-5678': { type: 'quarter', expiry: '2025-12-31', hwid: null },
    'ZP-L-TEST-9999': { type: 'lifetime', expiry: '2099-12-31', hwid: null }
};

// 序號激活端點
app.post('/activate', (req, res) => {
    const { serial, hwid } = req.body;
    
    if (!serial || !hwid) {
        return res.json({ success: false, message: '缺少序號或 HWID' });
    }
    
    const serialData = validSerials[serial];
    
    if (!serialData) {
        return res.json({ success: false, message: '序號無效或已過期' });
    }
    
    // 檢查 HWID 綁定
    if (serialData.hwid && serialData.hwid !== hwid) {
        return res.json({ success: false, message: '序號已綁定到其他電腦' });
    }
    
    // 綁定 HWID
    serialData.hwid = hwid;
    
    res.json({ 
        success: true, 
        message: '激活成功',
        type: serialData.type,
        expiry: serialData.expiry
    });
});

// 心跳驗證端點
app.post('/heartbeat', (req, res) => {
    const { serial, hwid } = req.body;
    
    const serialData = validSerials[serial];
    
    if (!serialData || serialData.hwid !== hwid) {
        return res.json({ allow: false, message: '驗證失敗' });
    }
    
    // 檢查過期
    const expiryDate = new Date(serialData.expiry);
    const now = new Date();
    
    if (now > expiryDate) {
        return res.json({ allow: false, message: '序號已過期' });
    }
    
    res.json({ allow: true, message: 'OK' });
});

// 健康檢查
app.get('/health', (req, res) => {
    res.json({ status: 'ZeroPulse API is running' });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`[*] ZeroPulse API 執行在 http://localhost:${PORT}`);
});
