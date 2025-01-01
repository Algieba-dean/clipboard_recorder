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
        self.config = config
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
            max_files = self.config.get(
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
        if not self.config.get(ConfigKeys.Logging.SECTION, ConfigKeys.Logging.SAVE_IMAGE_FILE):
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
            if len(image_data) > self.config.get(
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

    def save(self, content: ClipboardContent):
        """保存剪贴板内容到日志"""
        data_dict = content.to_dict()
        
        # 处理图片数据
        if (content.content_type == ContentType.IMAGE.value and
            JsonKeys.IMAGE_DATA in content.data):
            image_path = self._save_image(content)
            if image_path:
                data_dict[JsonKeys.IMAGE_PATH] = image_path
            if self.config.get(ConfigKeys.Logging.SECTION, ConfigKeys.Logging.SAVE_IMAGE_BASE64):
                data_dict[JsonKeys.IMAGE_BASE64] = content.data[JsonKeys.IMAGE_DATA]
            del data_dict[JsonKeys.IMAGE_DATA]
        
        # 读取现有数据
        log_file = self._get_log_file()
        existing_data = []
        
        # 尝试读取现有日志文件
        if os.path.exists(log_file):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    file_content = f.read().strip()
                    if file_content:  # 确保文件不是空的
                        existing_data = json.loads(file_content)
                        if not isinstance(existing_data, list):
                            existing_data = []
                        else:
                            # 按时间戳降序排序现有数据
                            existing_data.sort(
                                key=lambda x: x.get(JsonKeys.TIMESTAMP, ""),
                                reverse=True
                            )
            except (json.JSONDecodeError, Exception) as e:
                print(Messages.Error.READ_LOG_ERROR.format(str(e)))
                # 如果文件损坏，尝试备份
                if os.path.exists(log_file):
                    backup_file = f"{log_file}{FileFormat.BACKUP_FILE_SUFFIX}"
                    try:
                        os.rename(log_file, backup_file)
                        print(Messages.Error.BACKUP_LOG_MESSAGE.format(backup_file))
                    except Exception:
                        pass
        
        # 将新数据添加到列表
        existing_data.append(data_dict)
        
        # 按时间戳降序排序所有数据
        existing_data.sort(
            key=lambda x: x.get(JsonKeys.TIMESTAMP, ""),
            reverse=True
        )
        
        # 检查记录数量限制
        max_entries = self.config.get(
            ConfigKeys.Logging.SECTION,
            ConfigKeys.Logging.MAX_ENTRIES
        )
        if len(existing_data) > max_entries:
            existing_data = existing_data[:max_entries]
        
        # 保存到文件
        try:
            # 先写入临时文件
            temp_file = f"{log_file}{FileFormat.TEMP_FILE_SUFFIX}"
            with open(temp_file, 'w', encoding='utf-8') as f:
                indent = 2 if self.config.get(
                    ConfigKeys.Logging.SECTION,
                    ConfigKeys.Logging.INDENT_JSON
                ) else None
                json.dump(existing_data, f, ensure_ascii=False, indent=indent)
            
            # 如果写入成功，替换原文件
            if os.path.exists(log_file):
                os.replace(temp_file, log_file)
            else:
                os.rename(temp_file, log_file)
                
        except Exception as e:
            print(Messages.Error.SAVE_LOG_ERROR.format(str(e)))
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass 