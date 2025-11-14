@echo off
:: ZeroPulse 快速啟動指令碼

echo.
echo ========================================
echo    ZeroPulse 2.0 - 快速啟動
echo ========================================
echo.

REM 檢查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python 未安裝或不在 PATH 中
    echo 請先安裝 Python: https://www.python.org/
    pause
    exit /b 1
)

REM 安裝依賴
echo [*] 安裝 Python 依賴...
pip install pyautogui psutil -q
if %errorlevel% neq 0 (
    echo [!] 安裝失敗
    pause
    exit /b 1
)

REM 執行客戶端 GUI
echo [*] 啟動 ZeroPulse GUI...
cd client
python gui.py

if %errorlevel% neq 0 (
    echo [!] GUI 啟動失敗
    pause
    exit /b 1
)

pause
