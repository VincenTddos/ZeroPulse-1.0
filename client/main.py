# main.py - ZeroPulse 客戶端核心程式
# pip install pyautogui psutil

import json
import os
import uuid
from datetime import datetime

# ===== 17把槍彈道數據 (UC 2025 最新) =====
RECOIL_PATTERNS = {
    "ak": {
        "stand_vert": [0, 12, 22, 30, 36, 40, 42, 43, 43, 42, 41, 40, 38, 36, 34],
        "stand_hori": [0, 4, -7, 10, -12, 14, -15, 15, -14, 13, -12, 11, -10, 9, -8],
        "crouch_mult": 0.65
    },
    "lr300": {
        "stand_vert": [0, 10, 18, 25, 30, 33, 36, 38, 39, 39, 39, 38, 37, 36, 35],
        "stand_hori": [0, 3, -5, 7, -9, 11, -12, 12, -11, 10, -9, 8, -7, 6, -5],
        "crouch_mult": 0.70
    },
    "mp5": {
        "stand_vert": [0, 8, 15, 21, 25, 28, 30, 31, 31, 31, 30, 29, 28, 27, 26],
        "stand_hori": [0, 2, -3, 4, -5, 6, -6, 6, -5, 5, -4, 4, -3, 3, -2],
        "crouch_mult": 0.75
    },
    "tommy": {
        "stand_vert": [0, 10, 17, 24, 30, 34, 37, 39, 40, 40, 39, 38, 37, 36, 35],
        "stand_hori": [0, 5, -8, 10, -12, 14, -16, 17, -18, 19, -20, 21, -22, 23, -24],
        "crouch_mult": 0.72
    },
    "m249": {
        "stand_vert": [0, 20, 40, 55, 65, 72, 78, 82, 85, 87, 88, 89, 90, 91, 92] + [92]*50,
        "stand_hori": [0, 8, -12, 16, -20, 24, -28, 32, -36, 40, -44, 48, -52, 56, -60] + [0]*50,
        "crouch_mult": 0.60
    },
    "m92": {
        "stand_vert": [0, 6, 12, 16, 20, 22, 24, 25, 26, 27],
        "stand_hori": [0, 2, -3, 4, -5, 6, -7, 8, -8, 7],
        "crouch_mult": 0.85
    },
    "spas12": {
        "stand_vert": [0, 14, 24, 32, 39, 44, 47, 49, 50, 51],
        "stand_hori": [0, 4, -6, 8, -10, 12, -14, 16, -18, 20],
        "crouch_mult": 0.68
    },
    "python": {
        "stand_vert": [0, 8, 14, 19, 23, 25, 26, 27, 28, 29],
        "stand_hori": [0, 2, -4, 5, -7, 8, -9, 10, -11, 12],
        "crouch_mult": 0.82
    },
    "custom_smg": {
        "stand_vert": [0, 7, 13, 18, 22, 25, 27, 29, 30, 31, 32, 32, 31, 30, 29],
        "stand_hori": [0, 2, -3, 4, -5, 6, -7, 8, -9, 10, -10, 10, -9, 8, -7],
        "crouch_mult": 0.78
    },
    "sar": {
        "stand_vert": [0, 7, 13, 18, 22, 24, 26, 27, 28, 29],
        "stand_hori": [0, 2, -3, 4, -5, 6, -7, 8, -9, 10],
        "crouch_mult": 0.80
    },
    "hmlmg": {
        "stand_vert": [0, 17, 32, 45, 55, 62, 67, 70, 72, 73, 74] + [74]*50,
        "stand_hori": [0, 6, -10, 14, -18, 22, -26, 30, -34, 38, -42] + [0]*50,
        "crouch_mult": 0.62
    },
    "m39": {
        "stand_vert": [0, 10, 18, 25, 30, 33, 35, 36, 37, 38],
        "stand_hori": [0, 2, -4, 5, -7, 8, -9, 10, -11, 12],
        "crouch_mult": 0.75
    },
    "pump": {
        "stand_vert": [0, 12, 21, 28, 34, 38, 40, 41, 42, 43],
        "stand_hori": [0, 3, -5, 7, -9, 11, -12, 13, -14, 15],
        "crouch_mult": 0.70
    },
    "m39_rifle": {
        "stand_vert": [0, 4, 8, 11, 14, 16, 17, 18, 19, 20],
        "stand_hori": [0, 1, -2, 3, -4, 5, -5, 5, -5, 4],
        "crouch_mult": 0.90
    },
    "l96": {
        "stand_vert": [0, 5, 10, 13, 16, 18, 19, 20, 21, 22],
        "stand_hori": [0, 1, -2, 3, -4, 5, -5, 5, -5, 4],
        "crouch_mult": 0.88
    },
    "bolt": {
        "stand_vert": [0, 4, 8, 11, 13, 15, 16, 17, 18, 19],
        "stand_hori": [0, 1, -2, 3, -4, 5, -5, 5, -5, 4],
        "crouch_mult": 0.89
    }
}

class ZeroPulseClient:
    def __init__(self):
        self.hwid = self.get_hwid()
        self.licensed = False
        self.current_weapon = "ak"
        self.enabled = False
        self.sensitivity = 0.40
        self.mouse_mult = 1.25
        self.randomness = 15
        self.is_crouched = False
        
    def get_hwid(self):
        """取得主機板序號"""
        try:
            return str(uuid.getnode())
        except:
            return "HWID-UNKNOWN"
    
    def verify_license(self, serial):
        """簡單序號驗證"""
        # 測試序號
        valid_serials = {
            'ZP-M-TEST-1234': {'type': 'month', 'name': '月費'},
            'ZP-Q-TEST-5678': {'type': 'quarter', 'name': '季費'},
            'ZP-L-TEST-9999': {'type': 'lifetime', 'name': '終身'},
        }
        
        if serial in valid_serials:
            self.licensed = True
            plan_info = valid_serials[serial]
            return True, f"✓ 序號驗證成功！\n方案: {plan_info['name']}"
        else:
            return False, "❌ 序號無效或已過期！"
    
    def load_config(self):
        """載入設定檔"""
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.sensitivity = config.get('sensitivity', 0.40)
                self.mouse_mult = config.get('mouse_mult', 1.25)
                self.randomness = config.get('randomness', 15)
    
    def save_config(self):
        """保存設定檔"""
        config = {
            'sensitivity': self.sensitivity,
            'mouse_mult': self.mouse_mult,
            'randomness': self.randomness,
            'timestamp': datetime.now().isoformat()
        }
        config_file = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    
    def get_recoil_pattern(self, weapon):
        """取得武器彈道"""
        return RECOIL_PATTERNS.get(weapon, RECOIL_PATTERNS['ak'])
    
    def calculate_compensation(self, bullet_index, mult=1.0):
        """計算補償值"""
        pattern = self.get_recoil_pattern(self.current_weapon)
        
        if bullet_index >= len(pattern['stand_vert']):
            return 0, 0
        
        # 應用蹲壓倍數
        if self.is_crouched:
            mult *= pattern['crouch_mult']
        
        # 垂直後座 (下拉)
        vert = -pattern['stand_vert'][bullet_index] * mult * self.sensitivity * self.mouse_mult
        
        # 水平後座 (左右)
        hori_idx = bullet_index % len(pattern['stand_hori'])
        hori = -pattern['stand_hori'][hori_idx] * mult
        
        return int(hori), int(vert)

# 主程式進入點
if __name__ == "__main__":
    client = ZeroPulseClient()
    print(f"[*] ZeroPulse 客戶端初始化")
    print(f"[*] HWID: {client.hwid}")
    print(f"[*] 已載入 {len(RECOIL_PATTERNS)} 把槍的彈道數據")
