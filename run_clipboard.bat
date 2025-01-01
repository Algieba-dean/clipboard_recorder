@echo off
setlocal

:: 检查虚拟环境是否存在
if not exist "venv" (
    echo 正在创建虚拟环境...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo 正在安装依赖...
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    python venv\Scripts\pywin32_postinstall.py -install
) else (
    call venv\Scripts\activate.bat
)

:: 运行程序
python main.py

endlocal 