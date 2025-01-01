"""主程序入口"""
from src.monitor import ClipboardMonitor

def main():
    """主程序入口函数"""
    monitor = ClipboardMonitor()
    monitor.run()

if __name__ == "__main__":
    main() 