@echo off
chcp 65001 > nul
echo 正在更新文档...

:: 激活虚拟环境（如果存在）
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo 警告：未找到虚拟环境，使用系统 Python
)

:: 检查是否安装了必要的包
python -c "import sphinx" 2>nul
if errorlevel 1 (
    echo 正在安装必要的包...
    pip install sphinx sphinx-rtd-theme
)

:: 清理旧的构建文件
if exist docs\_build (
    echo 清理旧的构建文件...
    rd /s /q docs\_build
)

:: 创建必要的目录
if not exist docs\_static mkdir docs\_static
if not exist docs\_templates mkdir docs\_templates
if not exist docs\_build mkdir docs\_build

:: 构建文档
echo 正在生成文档...
sphinx-build -b html docs docs/_build/html

:: 如果生成成功，自动打开文档
if errorlevel 0 (
    echo 文档生成成功！
    echo 正在打开文档...
    start "" "docs\_build\html\index.html"
) else (
    echo 文档生成失败，请检查错误信息。
)

:: 如果是在虚拟环境中，则退出虚拟环境
if exist venv\Scripts\activate.bat (
    deactivate
)

pause 