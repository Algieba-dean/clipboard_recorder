@echo off
chcp 65001
echo 正在构建 Clipboard Recorder...

:: 检查 Python 环境
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python
    exit /b 1
)

:: 检查并安装必要的包
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo 正在安装 PyInstaller...
    pip install pyinstaller
)

:: 清理旧的构建文件
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
if exist "*.spec" del /f /q *.spec

:: 构建可执行文件
pyinstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "Clipboard Recorder" ^
    --icon assets/icon.ico ^
    --add-data "config.json;." ^
    --add-data "src;src" ^
    --collect-submodules src ^
    --hidden-import win32clipboard ^
    --hidden-import PIL ^
    --hidden-import pyperclip ^
    main.py

:: 检查构建结果
if exist "dist\Clipboard Recorder.exe" (
    echo [32m构建成功！[0m
    echo [36m可执行文件位置: dist\Clipboard Recorder.exe[0m
) else (
    echo [31m构建失败！[0m
)

echo.
echo 按任意键退出...
pause >nul 