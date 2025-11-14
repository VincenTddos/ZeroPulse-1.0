@echo off
:: 打包 ZeroPulse.exe

echo [*] 安裝 PyInstaller...
pip install pyinstaller -q

echo [*] 打包客戶端...
cd client
pyinstaller --onefile --windowed --name "ZeroPulse" gui.py

echo [*] 完成！
echo 執行檔位置: dist\ZeroPulse.exe

pause
