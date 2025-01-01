"""数据模型模块

此模块包含剪贴板内容的数据模型类，用于存储和处理剪贴板数据。

Classes:
    ClipboardContent: 剪贴板内容的数据模型类
"""
from typing import Dict, Any, Optional
from datetime import datetime
import hashlib
import base64
from .constants import ContentType, JsonKeys

class ClipboardContent:
    """剪贴板内容的数据模型类，负责内容的存储和处理。
    
    此类用于存储从剪贴板读取的各种类型的内容（文本、图片、文件路径等），
    并提供将内容转换为可序列化格式的方法。

    Attributes:
        timestamp (str): 内容的时间戳，ISO格式
        content_type (str): 内容类型，可以是 text、image 或 files
        formats (Dict[str, int]): 剪贴板中可用的格式信息
        data (Dict[str, Any]): 实际的内容数据，根据类型不同而不同
    """

    def __init__(self):
        """初始化一个新的剪贴板内容对象。
        
        设置当前时间戳，初始化为未知类型，创建空的格式和数据字典。
        """
        self.timestamp: str = datetime.now().isoformat()
        self.content_type: str = ContentType.UNKNOWN.value
        self.formats: Dict[str, int] = {}
        self.data: Dict[str, Any] = {}

    def to_dict(self) -> Dict[str, Any]:
        """将对象转换为可序列化的字典格式。

        Returns:
            Dict[str, Any]: 包含所有属性的字典，可以直接序列化为JSON
        """
        result = {
            JsonKeys.TIMESTAMP: self.timestamp,
            JsonKeys.CONTENT_TYPE: self.content_type,
            JsonKeys.AVAILABLE_FORMATS: self.formats
        }
        result.update(self.data)
        return result

    def get_hash(self) -> Optional[str]:
        """获取内容的MD5哈希值。

        根据内容类型计算相应内容的MD5哈希值，用于判断内容是否发生变化。

        Returns:
            Optional[str]: 内容的MD5哈希值，如果无法计算则返回None
        """
        if self.content_type == ContentType.IMAGE.value and JsonKeys.IMAGE_DATA in self.data:
            return hashlib.md5(base64.b64decode(self.data[JsonKeys.IMAGE_DATA])).hexdigest()
        elif self.content_type == ContentType.TEXT.value and JsonKeys.TEXT_CONTENT in self.data:
            return hashlib.md5(self.data[JsonKeys.TEXT_CONTENT].encode('utf-8')).hexdigest()
        elif self.content_type == ContentType.FILES.value and JsonKeys.FILE_PATHS in self.data:
            return hashlib.md5(str(self.data[JsonKeys.FILE_PATHS]).encode('utf-8')).hexdigest()
        return None 