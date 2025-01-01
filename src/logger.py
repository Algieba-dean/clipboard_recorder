"""日志管理模块"""
import os
import json
from datetime import datetime
import base64
from typing import List, Optional
from .constants import (
    ContentType, FileFormat, Paths, JsonKeys,
    ConfigKeys, Messages
)
from .models import ClipboardContent
from .config import Config

class ClipboardLogger:
    """负责日志和文件的管理，处理内容的持久化存储"""
    def __init__(self, config: Config):
        self._config = config
        self.base_dir = config.get(ConfigKeys.General.SECTION, ConfigKeys.General.BASE_DIR)
        self.images_dir = os.path.join(
            self.base_dir,
            config.get(ConfigKeys.General.SECTION, ConfigKeys.General.IMAGES_DIR)
        )
        self._ensure_directories()
        self._cleanup_old_logs()

    def _ensure_directories(self):
        """确保必要的目录存在"""
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)

    def _cleanup_old_logs(self):
        """清理旧的日志文件"""
        try:
            log_files = sorted([
                f for f in os.listdir(self.base_dir)
                if f.startswith(FileFormat.LOG_FILE_PREFIX)
            ])
            max_files = self._config.get(
                ConfigKeys.General.SECTION,
                ConfigKeys.General.MAX_LOG_FILES
            )
            if len(log_files) > max_files:
                for f in log_files[:-max_files]:
                    os.remove(os.path.join(self.base_dir, f))
        except Exception as e:
            print(Messages.Error.READ_LOG_ERROR.format(str(e)))

    def _get_log_file(self) -> str:
        """获取当天的日志文件路径"""
        today = datetime.now().strftime(FileFormat.LOG_FILE_DATE_FORMAT)
        return os.path.join(
            self.base_dir,
            f'{FileFormat.LOG_FILE_PREFIX}{today}{FileFormat.LOG_FILE_EXTENSION}'
        )

    def _save_image(self, content: ClipboardContent) -> Optional[str]:
        """保存图片并返回保存路径"""
        if not self._config.get(ConfigKeys.Logging.SECTION, ConfigKeys.Logging.SAVE_IMAGE_FILE):
            return None

        try:
            image_time = datetime.fromisoformat(content.timestamp)
            image_filename = (
                f"{FileFormat.IMAGE_FILE_PREFIX}"
                f"{image_time.strftime(FileFormat.IMAGE_FILE_DATE_FORMAT)}"
                f"{FileFormat.IMAGE_FILE_EXTENSION}"
            )
            image_path = os.path.join(self.images_dir, image_filename)
            
            image_data = base64.b64decode(content.data[JsonKeys.IMAGE_DATA])
            if len(image_data) > self._config.get(
                ConfigKeys.ContentTypes.SECTION,
                ConfigKeys.ContentTypes.MAX_IMAGE_SIZE
            ):
                print(Messages.Error.IMAGE_SIZE_LIMIT)
                return None

            with open(image_path, 'wb') as f:
                f.write(image_data)
            
            return os.path.join(Paths.DEFAULT_IMAGES_DIR, image_filename)
        except Exception as e:
            print(Messages.Error.SAVE_IMAGE_ERROR.format(str(e)))
            return None

    def _read_log_file(self, log_file: str) -> List[dict]:
        """读取日志文件内容"""
        if not os.path.exists(log_file):
            return []
            
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                data = json.loads(content)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, IOError) as e:
            print(Messages.Error.READ_LOG_ERROR.format(str(e)))
            self._backup_log_file(log_file)
            return []

    def _backup_log_file(self, log_file: str):
        """备份损坏的日志文件"""
        if not os.path.exists(log_file):
            return
            
        backup_file = f"{log_file}{FileFormat.BACKUP_FILE_SUFFIX}"
        try:
            os.rename(log_file, backup_file)
            print(Messages.Error.BACKUP_LOG_MESSAGE.format(backup_file))
        except OSError:
            pass

    def _write_log_file(self, log_file: str, data: List[dict]):
        """写入日志文件"""
        temp_file = f"{log_file}{FileFormat.TEMP_FILE_SUFFIX}"
        try:
            indent = 2 if self._config.get(
                ConfigKeys.Logging.SECTION,
                ConfigKeys.Logging.INDENT_JSON
            ) else None
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            
            os.replace(temp_file, log_file) if os.path.exists(log_file) else os.rename(temp_file, log_file)
        except (IOError, OSError) as e:
            print(Messages.Error.SAVE_LOG_ERROR.format(str(e)))
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except OSError:
                    pass

    def _process_image_data(self, content: ClipboardContent, data_dict: dict) -> dict:
        """处理图片数据"""
        if (content.content_type != ContentType.IMAGE.value or
            JsonKeys.IMAGE_DATA not in content.data):
            return data_dict
            
        image_path = self._save_image(content)
        if image_path:
            data_dict[JsonKeys.IMAGE_PATH] = image_path
            
        if self._config.get(ConfigKeys.Logging.SECTION, ConfigKeys.Logging.SAVE_IMAGE_BASE64):
            data_dict[JsonKeys.IMAGE_BASE64] = content.data[JsonKeys.IMAGE_DATA]
            
        del data_dict[JsonKeys.IMAGE_DATA]
        return data_dict

    def save(self, content: ClipboardContent):
        """保存剪贴板内容到日志"""
        data_dict = content.to_dict()
        data_dict = self._process_image_data(content, data_dict)
        
        log_file = self._get_log_file()
        existing_data = self._read_log_file(log_file)
        
        # 添加新数据并排序
        existing_data.append(data_dict)
        existing_data.sort(
            key=lambda x: x.get(JsonKeys.TIMESTAMP, ""),
            reverse=True
        )
        
        # 限制记录数量
        max_entries = self._config.get(
            ConfigKeys.Logging.SECTION,
            ConfigKeys.Logging.MAX_ENTRIES
        )
        if len(existing_data) > max_entries:
            existing_data = existing_data[:max_entries]
        
        self._write_log_file(log_file, existing_data) 