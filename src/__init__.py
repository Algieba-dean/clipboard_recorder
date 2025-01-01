"""剪贴板监控工具包"""
import os
import sys

# 添加包路径到 Python 路径
package_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from .models import ClipboardContent
from .config import Config
from .logger import ClipboardLogger
from .monitor import ClipboardMonitor

__all__ = [
    'ClipboardContent',
    'Config',
    'ClipboardLogger',
    'ClipboardMonitor'
] 