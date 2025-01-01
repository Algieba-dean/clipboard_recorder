"""主程序入口"""
import sys
from pathlib import Path
from typing import NoReturn

def setup_python_path() -> None:
    """配置 Python 路径"""
    # 添加项目根目录到 Python 路径
    current_dir = Path(__file__).parent.absolute()
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))

    # 如果是打包后的可执行文件,添加额外路径
    if getattr(sys, 'frozen', False):
        bundle_dir = Path(sys._MEIPASS)
        sys.path.insert(0, str(bundle_dir / 'src'))

def main() -> NoReturn:
    """
    主程序入口函数
    启动剪贴板监控器
    """
    from src.monitor import ClipboardMonitor
    
    setup_python_path()
    monitor = ClipboardMonitor()
    monitor.run()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)