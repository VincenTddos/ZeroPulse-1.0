# gui.py - ZeroPulse 官方級 GUI 介面
# pip install pyautogui

import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui
import threading
import time
from main import ZeroPulseClient, RECOIL_PATTERNS

class ZeroPulseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ZeroPulse 2.0")
        self.root.geometry("950x650")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(False, False)
        
        self.client = ZeroPulseClient()
        self.client.load_config()
        
        self.firing = False
        self.bullet_count = 0
        self.script_enabled = False
        self.auto_detect = True
        
        self.setup_ui()
        self.start_monitoring()
    
    def setup_ui(self):
        """建立使用者介面"""
        
        # === 頂部狀態列 ===
        top_frame = tk.Frame(self.root, bg="#2d2d2d", height=60)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)
        
        tk.Label(top_frame, text="ZeroPulse 2.0", font=("Arial", 18, "bold"), 
                fg="#00ff88", bg="#2d2d2d").pack(side="left", padx=15, pady=10)
        
        self.status_label = tk.Label(top_frame, text="Ready", fg="#00ff88", bg="#2d2d2d", font=("Arial", 10))
        self.status_label.pack(side="right", padx=15)
        
        # === 開關區 ===
        switch_frame = tk.Frame(self.root, bg="#1a1a1a")
        switch_frame.pack(pady=15)
        
        self.script_var = tk.BooleanVar(value=False)
        tk.Checkbutton(switch_frame, text="Script ON / OFF", variable=self.script_var, 
                      command=self.toggle_script, bg="#1a1a1a", fg="white", 
                      selectcolor="#333", font=("Arial", 11)).pack(side="left", padx=20)
        
        self.auto_var = tk.BooleanVar(value=True)
        tk.Checkbutton(switch_frame, text="Auto Detection", variable=self.auto_var,
                      bg="#1a1a1a", fg="white", selectcolor="#333", font=("Arial", 11)).pack(side="left", padx=20)
        
        # 武器選擇
        tk.Label(switch_frame, text="Weapon Selected:", fg="#888", bg="#1a1a1a").pack(side="left", padx=10)
        self.weapon_combo = ttk.Combobox(switch_frame, values=sorted(RECOIL_PATTERNS.keys()), 
                                         state="readonly", width=15)
        self.weapon_combo.set("ak")
        self.weapon_combo.pack(side="left", padx=5)
        self.weapon_combo.bind("<<ComboboxSelected>>", self.on_weapon_change)
        
        self.stance_label = tk.Label(switch_frame, text="Stance: Standing", fg="#ffaa00", bg="#1a1a1a")
        self.stance_label.pack(side="left", padx=20)
        
        # === 設定分頁 ===
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=20, pady=10)
        
        # 設定頁
        settings_tab = tk.Frame(notebook, bg="#1a1a1a")
        notebook.add(settings_tab, text="Settings")
        
        # Aim Settings
        aim_frame = tk.LabelFrame(settings_tab, text="Aim Settings", fg="#00ff88", bg="#1a1a1a")
        aim_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(aim_frame, text="Sensitivity", fg="white", bg="#1a1a1a").pack(anchor="w", padx=10, pady=5)
        self.sens_scale = tk.Scale(aim_frame, from_=0.1, to=2.0, resolution=0.05, orient="horizontal",
                                  bg="#1a1a1a", fg="white", troughcolor="#333", command=self.update_sens)
        self.sens_scale.set(self.client.sensitivity)
        self.sens_scale.pack(fill="x", padx=10)
        
        tk.Label(aim_frame, text="Mouse Multiplier", fg="white", bg="#1a1a1a").pack(anchor="w", padx=10, pady=5)
        self.mult_scale = tk.Scale(aim_frame, from_=0.5, to=3.0, resolution=0.05, orient="horizontal",
                                  bg="#1a1a1a", fg="white", troughcolor="#333", command=self.update_mult)
        self.mult_scale.set(self.client.mouse_mult)
        self.mult_scale.pack(fill="x", padx=10)
        
        # General Settings
        gen_frame = tk.LabelFrame(settings_tab, text="General Settings", fg="#00ff88", bg="#1a1a1a")
        gen_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        tk.Label(gen_frame, text="Randomness (Humanize)", fg="white", bg="#1a1a1a").pack(anchor="w", padx=10, pady=5)
        self.rand_scale = tk.Scale(gen_frame, from_=0, to=50, resolution=1, orient="horizontal",
                                  bg="#1a1a1a", fg="white", troughcolor="#333", command=self.update_random)
        self.rand_scale.set(self.client.randomness)
        self.rand_scale.pack(fill="x", padx=10)
        
        self.rand_label = tk.Label(gen_frame, text=f"{self.client.randomness}%", fg="#00ff88", bg="#1a1a1a")
        self.rand_label.pack(anchor="e", padx=10)
        
        # === 底部信息 ===
        footer = tk.Frame(self.root, bg="#1a1a1a")
        footer.pack(fill="x", padx=20, pady=10)
        
        tk.Label(footer, text=f"HWID: {self.client.hwid}", fg="#666", bg="#1a1a1a", font=("Arial", 9)).pack(side="left")
        
        # 序號驗證按鈕
        tk.Button(footer, text="驗證序號", command=self.verify_serial, bg="#00ff88", fg="black", 
                 font=("Arial", 9)).pack(side="right", padx=5)
    
    def toggle_script(self):
        """切換腳本開關"""
        self.script_enabled = self.script_var.get()
        if self.script_enabled:
            if not self.client.licensed:
                messagebox.showerror("錯誤", "請先驗證序號！")
                self.script_var.set(False)
                self.script_enabled = False
                return
            self.status_label.config(text="ACTIVATED", fg="#00ff88")
        else:
            self.status_label.config(text="Ready", fg="#00ff88")
    
    def on_weapon_change(self, event=None):
        """武器變更"""
        self.client.current_weapon = self.weapon_combo.get()
    
    def update_sens(self, value):
        """更新靈敏度"""
        self.client.sensitivity = float(value)
        self.client.save_config()
    
    def update_mult(self, value):
        """更新滑鼠倍數"""
        self.client.mouse_mult = float(value)
        self.client.save_config()
    
    def update_random(self, value):
        """更新隨機度"""
        self.client.randomness = int(value)
        self.rand_label.config(text=f"{value}%")
        self.client.save_config()
    
    def verify_serial(self):
        """序號驗證視窗"""
        verify_window = tk.Toplevel(self.root)
        verify_window.title("序號驗證")
        verify_window.geometry("350x200")
        verify_window.configure(bg="#1a1a1a")
        
        tk.Label(verify_window, text="輸入序號激活碼", fg="#00ff88", bg="#1a1a1a", 
                font=("Arial", 12, "bold")).pack(pady=15)
        
        serial_entry = tk.Entry(verify_window, bg="#2d2d2d", fg="white", font=("Arial", 11))
        serial_entry.pack(padx=20, pady=10, fill="x")
        
        def verify():
            serial = serial_entry.get().strip()
            success, message = self.client.verify_license(serial)
            if success:
                messagebox.showinfo("成功", message)
                self.status_label.config(text="LICENSED", fg="#00ff88")
                verify_window.destroy()
            else:
                messagebox.showerror("失敗", message)
        
        tk.Button(verify_window, text="驗證", command=verify, bg="#00ff88", fg="black",
                 font=("Arial", 10)).pack(pady=20)
        
        # 顯示測試序號
        test_text = tk.Label(verify_window, text="測試序號: ZP-M-TEST-1234", fg="#666", bg="#1a1a1a")
        test_text.pack(pady=10)
    
    def start_monitoring(self):
        """啟動監控線程"""
        def monitor():
            while True:
                if self.script_enabled:
                    # 模擬滑鼠補償邏輯
                    # 實際應用會讀取 Rust 記憶體和輸入狀態
                    pass
                time.sleep(0.1)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()

def main():
    root = tk.Tk()
    gui = ZeroPulseGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
