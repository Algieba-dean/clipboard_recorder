"""监控管理模块"""
import os
import json
import time
import hashlib
import win32clipboard
import win32con
import pyperclip
from PIL import ImageGrab, Image
import io
import base64
from typing import Dict, Optional
from .constants import (
    ContentType, FileFormat, JsonKeys,
    ConfigKeys, Messages
)
from .models import ClipboardContent
from .config import Config
from .logger import ClipboardLogger

class ClipboardMonitor:
    """程序的核心类，负责监控和处理剪贴板变化"""
    def __init__(self):
        self.config = Config()
        self.logger = ClipboardLogger(self.config)
        self.last_hash: Optional[str] = None
        self._load_last_hash()

    def _load_last_hash(self):
        """从日志文件中加载最后一条记录的哈希值"""
        log_file = self.logger._get_log_file()
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        data = json.loads(content)
                        if isinstance(data, list) and len(data) > 0:
                            last_entry = data[0]  # 获取最新的记录
                            if (last_entry.get(JsonKeys.CONTENT_TYPE) == ContentType.TEXT.value
                                and JsonKeys.TEXT_CONTENT in last_entry):
                                self.last_hash = hashlib.md5(
                                    last_entry[JsonKeys.TEXT_CONTENT].encode('utf-8')
                                ).hexdigest()
                            elif (last_entry.get(JsonKeys.CONTENT_TYPE) == ContentType.IMAGE.value
                                  and JsonKeys.IMAGE_BASE64 in last_entry):
                                self.last_hash = hashlib.md5(
                                    base64.b64decode(last_entry[JsonKeys.IMAGE_BASE64])
                                ).hexdigest()
                            elif (last_entry.get(JsonKeys.CONTENT_TYPE) == ContentType.FILES.value
                                  and JsonKeys.FILE_PATHS in last_entry):
                                self.last_hash = hashlib.md5(
                                    str(last_entry[JsonKeys.FILE_PATHS]).encode('utf-8')
                                ).hexdigest()
            except Exception as e:
                print(Messages.Error.LOAD_HISTORY_ERROR.format(str(e)))

    def _get_clipboard_formats(self) -> Dict[str, int]:
        """获取剪贴板格式信息"""
        formats = {}
        try:
            win32clipboard.OpenClipboard()
            format_id = 0
            while True:
                try:
                    format_id = win32clipboard.EnumClipboardFormats(format_id)
                    if not format_id:
                        break
                    try:
                        format_name = win32clipboard.GetClipboardFormatName(format_id)
                    except:
                        format_name = f"Unknown Format ({format_id})"
                    formats[format_name] = format_id
                except:
                    break
            return formats
        finally:
            win32clipboard.CloseClipboard()

    def _read_clipboard(self) -> Optional[ClipboardContent]:
        """读取剪贴板内容"""
        try:
            content = ClipboardContent()
            content.formats = self._get_clipboard_formats()
            
            # 尝试获取图片
            if self.config.get(ConfigKeys.ContentTypes.SECTION, ConfigKeys.ContentTypes.ENABLE_IMAGE):
                try:
                    image = ImageGrab.grabclipboard()
                    if isinstance(image, Image.Image):
                        # 如果是PIL Image对象，直接处理
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format=FileFormat.IMAGE_FORMAT)
                        img_byte_arr = img_byte_arr.getvalue()
                        if len(img_byte_arr) <= self.config.get(
                            ConfigKeys.ContentTypes.SECTION,
                            ConfigKeys.ContentTypes.MAX_IMAGE_SIZE
                        ):
                            content.data[JsonKeys.IMAGE_DATA] = base64.b64encode(img_byte_arr).decode('utf-8')
                            content.content_type = ContentType.IMAGE.value
                            return content
                    elif isinstance(image, list) and len(image) > 0 and os.path.isfile(image[0]):
                        # 如果是文件路径列表（某些系统可能返回这种格式）
                        try:
                            with Image.open(image[0]) as img:
                                img_byte_arr = io.BytesIO()
                                img.save(img_byte_arr, format=FileFormat.IMAGE_FORMAT)
                                img_byte_arr = img_byte_arr.getvalue()
                                if len(img_byte_arr) <= self.config.get(
                                    ConfigKeys.ContentTypes.SECTION,
                                    ConfigKeys.ContentTypes.MAX_IMAGE_SIZE
                                ):
                                    content.data[JsonKeys.IMAGE_DATA] = base64.b64encode(img_byte_arr).decode('utf-8')
                                    content.content_type = ContentType.IMAGE.value
                                    return content
                        except Exception as e:
                            print(Messages.Error.PROCESS_IMAGE_ERROR.format(str(e)))
                except Exception as e:
                    print(Messages.Error.GET_CLIPBOARD_IMAGE_ERROR.format(str(e)))
            
            # 尝试获取文本
            if self.config.get(ConfigKeys.ContentTypes.SECTION, ConfigKeys.ContentTypes.ENABLE_TEXT):
                try:
                    text = pyperclip.paste()
                    if text:
                        if len(text) <= self.config.get(
                            ConfigKeys.ContentTypes.SECTION,
                            ConfigKeys.ContentTypes.MAX_TEXT_LENGTH
                        ):
                            content.data[JsonKeys.TEXT_CONTENT] = text
                            content.content_type = ContentType.TEXT.value
                            return content
                except Exception as e:
                    print(Messages.Error.GET_CLIPBOARD_TEXT_ERROR.format(str(e)))
            
            # 尝试获取文件路径
            if self.config.get(ConfigKeys.ContentTypes.SECTION, ConfigKeys.ContentTypes.ENABLE_FILES):
                try:
                    win32clipboard.OpenClipboard()
                    if win32clipboard.IsClipboardFormatAvailable(win32con.CF_HDROP):
                        content.data[JsonKeys.FILE_PATHS] = win32clipboard.GetClipboardData(win32con.CF_HDROP)
                        content.content_type = ContentType.FILES.value
                        return content
                except Exception as e:
                    print(Messages.Error.GET_CLIPBOARD_FILES_ERROR.format(str(e)))
                finally:
                    try:
                        win32clipboard.CloseClipboard()
                    except:
                        pass
            
            return None
        except Exception as e:
            print(Messages.Error.MONITOR_ERROR.format(str(e)))
            return None

    def _print_content(self, content: ClipboardContent):
        """打印剪贴板内容信息"""
        if not self.config.get(ConfigKeys.Display.SECTION, ConfigKeys.Display.SHOW_PREVIEW):
            return

        print(Messages.Info.CLIPBOARD_CONTENT_HEADER)
        print("-" * self.config.get(ConfigKeys.Display.SECTION, ConfigKeys.Display.CONSOLE_WIDTH))
        print(f"内容类型: {content.content_type}")
        
        display_data = content.to_dict()
        if JsonKeys.IMAGE_DATA in display_data:
            del display_data[JsonKeys.IMAGE_DATA]
        if JsonKeys.IMAGE_BASE64 in display_data:
            del display_data[JsonKeys.IMAGE_BASE64]
        
        if self.config.get(ConfigKeys.Display.SECTION, ConfigKeys.Display.SHOW_TIMESTAMPS):
            print(f"时间: {content.timestamp}")
        
        # 截断预览内容
        max_length = self.config.get(ConfigKeys.Display.SECTION, ConfigKeys.Display.MAX_PREVIEW_LENGTH)
        if JsonKeys.TEXT_CONTENT in display_data and len(display_data[JsonKeys.TEXT_CONTENT]) > max_length:
            display_data[JsonKeys.TEXT_CONTENT] = display_data[JsonKeys.TEXT_CONTENT][:max_length] + "..."
        
        print(json.dumps(display_data, indent=2, ensure_ascii=False))
        print("-" * self.config.get(ConfigKeys.Display.SECTION, ConfigKeys.Display.CONSOLE_WIDTH))
        print(Messages.Info.CONTENT_SAVED)

    def check_and_save(self) -> bool:
        """检查剪贴板并保存新内容"""
        content = self._read_clipboard()
        if not content:
            return False
        
        content_hash = content.get_hash()
        if not content_hash or content_hash == self.last_hash:
            return False
        
        self.logger.save(content)
        self._print_content(content)
        self.last_hash = content_hash
        return True

    def run(self):
        """运行监控程序"""
        print(Messages.Info.MONITOR_START)
        try:
            while True:
                try:
                    self.check_and_save()
                except Exception as e:
                    print(Messages.Error.MONITOR_ERROR.format(str(e)))
                time.sleep(self.config.get(ConfigKeys.General.SECTION, ConfigKeys.General.CHECK_INTERVAL))
        except KeyboardInterrupt:
            print(Messages.Info.MONITOR_STOP) 