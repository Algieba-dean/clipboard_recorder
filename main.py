"""主程序入口"""
import os
import sys

# 添加项目根目录到 Python 路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if getattr(sys, 'frozen', False):
    # 如果是打包后的可执行文件
    bundle_dir = sys._MEIPASS
    sys.path.insert(0, os.path.join(bundle_dir, 'src'))

from src.monitor import ClipboardMonitor

def main():
    """主程序入口函数"""
    monitor = ClipboardMonitor()
    monitor.run()

if __name__ == "__main__":
    main() 