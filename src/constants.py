"""常量定义模块

此模块定义了程序中使用的所有常量，包括内容类型、文件格式、路径、配置键名等。
使用枚举和类来组织常量，提供更好的类型提示和代码组织。

Classes:
    ContentType: 内容类型枚举
    FileFormat: 文件格式相关常量
    Paths: 路径相关常量
    JsonKeys: JSON键名常量
    ConfigKeys: 配置键名常量
    DefaultConfig: 默认配置常量
    Messages: 提示信息常量
"""
from enum import Enum

class ContentType(Enum):
    """内容类型枚举。
    
    定义了支持的剪贴板内容类型。

    Attributes:
        UNKNOWN: 未知类型
        TEXT: 文本内容
        IMAGE: 图片内容
        FILES: 文件路径
    """
    UNKNOWN = "unknown"
    TEXT = "text"
    IMAGE = "image"
    FILES = "files"

class FileFormat:
    """文件格式相关常量。
    
    定义了日志文件和图片文件的命名格式。

    Attributes:
        LOG_FILE_PREFIX: 日志文件名前缀
        LOG_FILE_DATE_FORMAT: 日志文件日期格式
        LOG_FILE_EXTENSION: 日志文件扩展名
        IMAGE_FILE_PREFIX: 图片文件名前缀
        IMAGE_FILE_DATE_FORMAT: 图片文件日期格式
        IMAGE_FILE_EXTENSION: 图片文件扩展名
        IMAGE_FORMAT: 图片保存格式
        TEMP_FILE_SUFFIX: 临时文件后缀
        BACKUP_FILE_SUFFIX: 备份文件后缀
    """
    # 日志文件格式
    LOG_FILE_PREFIX = "clipboard_"
    LOG_FILE_DATE_FORMAT = "%Y-%m-%d"
    LOG_FILE_EXTENSION = ".json"
    
    # 图片文件格式
    IMAGE_FILE_PREFIX = "clipboard_image_"
    IMAGE_FILE_DATE_FORMAT = "%Y%m%d_%H%M%S"
    IMAGE_FILE_EXTENSION = ".png"
    IMAGE_FORMAT = "PNG"
    
    # 临时文件后缀
    TEMP_FILE_SUFFIX = ".temp"
    BACKUP_FILE_SUFFIX = ".backup"

class Paths:
    """路径相关常量。
    
    定义了程序使用的默认路径。

    Attributes:
        DEFAULT_BASE_DIR: 默认的日志根目录
        DEFAULT_IMAGES_DIR: 默认的图片存储目录
        DEFAULT_CONFIG_FILE: 默认的配置文件路径
    """
    DEFAULT_BASE_DIR = "logs"
    DEFAULT_IMAGES_DIR = "images"
    DEFAULT_CONFIG_FILE = "config.json"

class JsonKeys:
    """JSON键名常量。
    
    定义了JSON数据中使用的所有键名。

    Attributes:
        TIMESTAMP: 时间戳键名
        CONTENT_TYPE: 内容类型键名
        AVAILABLE_FORMATS: 可用格式键名
        TEXT_CONTENT: 文本内容键名
        IMAGE_DATA: 图片数据键名
        IMAGE_PATH: 图片路径键名
        IMAGE_BASE64: 图片base64键名
        FILE_PATHS: 文件路径键名
    """
    TIMESTAMP = "timestamp"
    CONTENT_TYPE = "content_type"
    AVAILABLE_FORMATS = "available_formats"
    TEXT_CONTENT = "text_content"
    IMAGE_DATA = "image_data"
    IMAGE_PATH = "image_path"
    IMAGE_BASE64 = "image_base64"
    FILE_PATHS = "file_paths"

class ConfigKeys:
    """配置键名常量。
    
    定义了配置文件中使用的所有键名，按功能分组。
    """
    class General:
        """常规设置键名"""
        SECTION = "general"
        CHECK_INTERVAL = "check_interval"
        MAX_LOG_FILES = "max_log_files"
        BASE_DIR = "base_dir"
        IMAGES_DIR = "images_dir"

    class Logging:
        """日志设置键名"""
        SECTION = "logging"
        SAVE_IMAGE_FILE = "save_image_file"
        SAVE_IMAGE_BASE64 = "save_image_base64"
        MAX_ENTRIES = "max_entries_per_file"
        INDENT_JSON = "indent_json"

    class ContentTypes:
        """内容类型设置键名"""
        SECTION = "content_types"
        ENABLE_TEXT = "enable_text"
        ENABLE_IMAGE = "enable_image"
        ENABLE_FILES = "enable_files"
        MAX_TEXT_LENGTH = "max_text_length"
        MAX_IMAGE_SIZE = "max_image_size"

    class Display:
        """显示设置键名"""
        SECTION = "display"
        SHOW_PREVIEW = "show_content_preview"
        MAX_PREVIEW_LENGTH = "max_preview_length"
        SHOW_TIMESTAMPS = "show_timestamps"
        CONSOLE_WIDTH = "console_width"

class DefaultConfig:
    """默认配置常量。
    
    定义了所有配置项的默认值。

    Attributes:
        DEFAULT_CONFIG: 包含所有默认配置的字典
    """
    DEFAULT_CONFIG = {
        ConfigKeys.General.SECTION: {
            ConfigKeys.General.CHECK_INTERVAL: 1.0,
            ConfigKeys.General.MAX_LOG_FILES: 30,
            ConfigKeys.General.BASE_DIR: Paths.DEFAULT_BASE_DIR,
            ConfigKeys.General.IMAGES_DIR: Paths.DEFAULT_IMAGES_DIR
        },
        ConfigKeys.Logging.SECTION: {
            ConfigKeys.Logging.SAVE_IMAGE_FILE: True,
            ConfigKeys.Logging.SAVE_IMAGE_BASE64: True,
            ConfigKeys.Logging.MAX_ENTRIES: 1000,
            ConfigKeys.Logging.INDENT_JSON: True
        },
        ConfigKeys.ContentTypes.SECTION: {
            ConfigKeys.ContentTypes.ENABLE_TEXT: True,
            ConfigKeys.ContentTypes.ENABLE_IMAGE: True,
            ConfigKeys.ContentTypes.ENABLE_FILES: True,
            ConfigKeys.ContentTypes.MAX_TEXT_LENGTH: 1000000,
            ConfigKeys.ContentTypes.MAX_IMAGE_SIZE: 10485760
        },
        ConfigKeys.Display.SECTION: {
            ConfigKeys.Display.SHOW_PREVIEW: True,
            ConfigKeys.Display.MAX_PREVIEW_LENGTH: 200,
            ConfigKeys.Display.SHOW_TIMESTAMPS: True,
            ConfigKeys.Display.CONSOLE_WIDTH: 80
        }
    }

class Messages:
    """提示信息常量。
    
    定义了程序中使用的所有提示信息。
    """
    class Error:
        """错误信息常量"""
        CONFIG_LOAD_ERROR = "加载配置文件时发生错误：{}"
        USE_DEFAULT_CONFIG = "使用默认配置"
        READ_LOG_ERROR = "读取日志文件时发生错误：{}"
        BACKUP_LOG_MESSAGE = "已将损坏的日志文件备份为：{}"
        SAVE_LOG_ERROR = "保存日志文件时发生错误：{}"
        IMAGE_SIZE_LIMIT = "图片大小超过限制，跳过保存"
        SAVE_IMAGE_ERROR = "保存图片时发生错误：{}"
        PROCESS_IMAGE_ERROR = "处理图片文件时发生错误：{}"
        GET_CLIPBOARD_IMAGE_ERROR = "获取剪贴板图片时发生错误：{}"
        GET_CLIPBOARD_TEXT_ERROR = "获取剪贴板文本时发生错误：{}"
        GET_CLIPBOARD_FILES_ERROR = "获取剪贴板文件路径时发生错误：{}"
        MONITOR_ERROR = "监控时发生错误：{}"
        LOAD_HISTORY_ERROR = "加载历史记录时发生错误：{}"

    class Info:
        """提示信息常量"""
        MONITOR_START = "剪贴板监控已启动..."
        MONITOR_STOP = "\n程序已停止"
        CONTENT_SAVED = "内容已保存到日志文件中"
        CLIPBOARD_CONTENT_HEADER = "\n剪贴板内容和元数据：" 