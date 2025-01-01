# Windows 剪贴板内容读取工具

一个用于读取 Windows 剪贴板内容和元数据的 Python 工具，可以获取剪贴板中的文本、图片、格式信息和文件路径等信息。

## 📋 功能介绍

- ✅ 读取剪贴板中的文本内容
- 📸 支持图片内容的获取和保存
  - 保存为物理文件
  - 同时保存 base64 编码到日志
- 📊 获取剪贴板数据的所有可用格式
- 📂 获取复制文件的完整路径（当复制文件时）
- ⏰ 记录操作时间戳
- 🔍 以 JSON 格式展示所有信息
- 💾 自动保存每天的剪贴板历史
- 🔄 支持持续监控模式
- 🎯 智能去重，避免重复记录相同内容
- ⏱️ 按时间倒序存储，最新内容始终在前

## 🔧 环境要求

- Windows 操作系统
- Python 3.6+
- 首次安装需要管理员权限

## 🚀 快速开始

### 1. 下载文件
确保以下文件在同一文件夹中：
- `run_clipboard.bat`
- `clipboard_reader.py`
- `requirements.txt`

### 2. 首次运行设置
1. 右键点击 `run_clipboard.bat`
2. 选择 "以管理员身份运行"
3. 等待自动完成以下操作：
   - 创建 Python 虚拟环境
   - 安装必要的依赖包
   - 配置 pywin32

### 3. 使用方式
有两种运行模式：

#### 单次读取模式
- 直接双击 `run_clipboard.bat`
- 程序会读取当前剪贴板内容并保存

#### 持续监控模式（推荐）
- 双击 `run_clipboard.bat`
- 程序会持续运行并监控剪贴板变化
- 每当剪贴板内容改变时自动保存
- 按 `Ctrl+C` 可以停止程序

### 4. 日志文件
- 所有复制的内容会自动保存在 `logs` 文件夹中
- 文本内容和元数据保存在日期文件中（格式：`clipboard_YYYY-MM-DD.json`）
- 图片内容保存在 `logs/images` 目录下（格式：`clipboard_image_YYYYMMDD_HHMMSS.png`）
- 内容按时间倒序存储，最新的记录总是在文件开头
- 可以随时查看历史复制记录

## 📝 输出示例

### 文本内容
```json
{
    "timestamp": "2024-01-20T12:34:56.789",
    "content_type": "text",
    "available_formats": {
        "CF_TEXT": 1,
        "CF_UNICODETEXT": 13,
        "HTML Format": 49383
    },
    "text_content": "示例文本内容"
}
```

### 图片内容
```json
{
    "timestamp": "2024-01-20T12:34:56.789",
    "content_type": "image",
    "available_formats": {
        "CF_BITMAP": 2,
        "PNG": 17
    },
    "image_path": "images/clipboard_image_20240120_123456.png",
    "image_base64": "data:image/png;base64,..."  // 完整的base64图片数据
}
```

## 📁 项目结构

```
clipboard_thief/
├── main.py              # 主程序入口
├── requirements.txt     # Python 依赖包列表
├── run_clipboard.bat    # 运行脚本（包含环境配置）
├── README.md           # 说明文档
├── config.json         # 配置文件（可选）
└── src/               # 源代码目录
    ├── __init__.py    # 包初始化文件
    ├── constants.py   # 常量定义
    ├── models.py      # 数据模型
    ├── config.py      # 配置管理
    ├── logger.py      # 日志管理
    └── monitor.py     # 监控管理
```

## 🔨 代码组织架构

### 1. 核心类设计

#### ClipboardContent（数据模型）
```python
"""剪贴板内容的数据模型类，负责内容的存储和处理"""
class ClipboardContent:
    # 属性
    - timestamp: str          # 内容的时间戳
    - content_type: str       # 内容类型（text/image/files）
    - formats: Dict[str, int] # 剪贴板格式信息
    - data: Dict[str, Any]    # 实际内容数据
    
    # 方法
    + to_dict() -> Dict      # 转换为可序列化的字典
    + get_hash() -> str      # 获取内容的唯一哈希值
```

#### ClipboardLogger（日志管理）
```python
"""负责日志和文件的管理，处理内容的持久化存储"""
class ClipboardLogger:
    # 属性
    - base_dir: str          # 日志根目录
    - images_dir: str        # 图片存储目录
    - config: Config         # 配置对象
    
    # 公共方法
    + save()                 # 保存内容到日志
    
    # 私有方法
    - _ensure_directories()  # 确保目录存在
    - _get_log_file() -> str # 获取日志文件路径
    - _save_image() -> str   # 保存图片文件
    - _cleanup_old_logs()    # 清理旧日志文件
```

#### ClipboardMonitor（监控管理）
```python
"""程序的核心类，负责监控和处理剪贴板变化"""
class ClipboardMonitor:
    # 属性
    - logger: ClipboardLogger # 日志管理器
    - config: Config         # 配置对象
    - last_hash: str         # 上一次内容的哈希值
    
    # 公共方法
    + run()                  # 运行监控程序
    + check_and_save()       # 检查并保存新内容
    
    # 私有方法
    - _read_clipboard()      # 读取剪贴板内容
    - _get_clipboard_formats() # 获取格式信息
    - _print_content()       # 打印内容信息
    - _load_last_hash()      # 加载最后一条记录的哈希值
```

#### Config（配置管理）
```python
"""配置管理类，负责加载和管理配置"""
class Config:
    # 属性
    - config_file: str       # 配置文件路径
    - config: Dict           # 配置数据
    
    # 公共方法
    + get()                  # 获取配置值
    
    # 私有方法
    - _load_config()         # 加载配置文件
    - _merge_config()        # 合并配置
```

### 2. 常量管理
项目使用专门的常量管理模块（`src/constants.py`），包含以下部分：

#### ContentType（枚举）
```python
"""内容类型枚举"""
class ContentType(Enum):
    UNKNOWN = "unknown"      # 未知类型
    TEXT = "text"           # 文本内容
    IMAGE = "image"         # 图片内容
    FILES = "files"         # 文件路径
```

#### FileFormat（常量类）
```python
"""文件格式相关常量"""
class FileFormat:
    # 日志文件格式
    LOG_FILE_PREFIX = "clipboard_"
    LOG_FILE_DATE_FORMAT = "%Y-%m-%d"
    LOG_FILE_EXTENSION = ".json"
    
    # 图片文件格式
    IMAGE_FILE_PREFIX = "clipboard_image_"
    IMAGE_FILE_DATE_FORMAT = "%Y%m%d_%H%M%S"
    IMAGE_FILE_EXTENSION = ".png"
    IMAGE_FORMAT = "PNG"
```

### 3. 模块依赖关系
```
main.py
└── src.monitor
    ├── .constants
    ├── .models
    │   └── .constants
    ├── .config
    │   └── .constants
    └── .logger
        ├── .constants
        ├── .models
        └── .config
```

### 4. 设计特点
- **模块化设计**: 代码按功能拆分为独立模块
- **单一职责**: 每个类都有明确的职责
- **封装性**: 内部实现细节对外部不可见
- **可扩展性**: 容易添加新的内容类型和处理方式
- **可维护性**: 逻辑清晰，代码结构规范
- **类型安全**: 使用类型注解确保类型安全
- **常量管理**: 统一管理所有常量，避免硬编码
- **配置灵活**: 支持自定义配置，有合理默认值

### 5. 错误处理
- 所有关键操作都有异常处理
- 文件操作错误不会影响程序运行
- 剪贴板访问错误会被优雅处理
- 日志记录失败不会中断监控
- 配置加载失败会使用默认值

## ❗ 常见问题解决

### 模块未找到错误
如果遇到 "ModuleNotFoundError: No module named 'win32clipboard'" 错误：
1. 删除 venv 文件夹
2. 以管理员身份重新运行 `run_clipboard.bat`

### 其他问题
- 确保使用 Windows 系统
- 检查 Python 是否正确安装
- 验证是否有管理员权限

## 📌 注意事项

1. 首次运行必须使用管理员权限
2. 仅支持 Windows 操作系统
3. 某些特殊格式的剪贴板内容可能无法完全读取
4. 建议使用最新版本的 Python
5. 持续监控模式会每秒检查一次剪贴板变化
6. 图片会同时保存为物理文件和 base64 格式
7. 日志文件可能会较大，因为包含了 base64 编码的图片数据

## 🔄 更新日志

### v1.5.0
- 添加配置文件支持
- 增加更多可自定义选项
- 添加配置说明文档

### v1.4.0
- 添加按时间倒序存储功能
- 优化日志文件读取体验

### v1.3.0
- 添加图片 base64 编码存储
- 优化内容重复检测
- 改进日志文件格式

### v1.2.0
- 添加图片内容的获取和保存功能
- 优化内容类型识别
- 添加图片存储目录

### v1.1.0
- 添加持续监控模式
- 添加按天保存日志功能
- 优化日志文件结构

### v1.0.0
- 初始版本发布
- 支持基本的剪贴板内容读取
- 支持文件路径获取
- 支持格式信息显示

## 🔧 配置说明

程序提供了灵活的配置选项，可以通过修改 `config.json` 文件来自定义行为：

- **常规设置**: 检查间隔、日志保留时间等
- **日志设置**: 图片保存方式、日志格式等
- **内容类型**: 启用/禁用特定类型的内容记录
- **显示设置**: 自定义控制台输出格式

详细的配置说明请参考 `config.md` 文件。
