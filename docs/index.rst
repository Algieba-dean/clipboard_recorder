Clipboard Recorder 文档
=====================

欢迎来到 Clipboard Recorder 的文档！

.. toctree::
   :maxdepth: 2
   :caption: 目录:

   modules/models
   modules/config
   modules/constants
   modules/logger
   modules/monitor

功能模块
--------

* :mod:`src.models`: 数据模型模块，定义了剪贴板内容的数据结构
* :mod:`src.config`: 配置管理模块，处理程序配置的加载和访问
* :mod:`src.constants`: 常量定义模块，包含所有程序使用的常量
* :mod:`src.logger`: 日志管理模块，负责内容的持久化存储
* :mod:`src.monitor`: 监控管理模块，负责监控和处理剪贴板变化

功能特性
--------

* 支持多种内容类型：文本、图片、文件路径
* 自动保存剪贴板历史记录
* 可配置的内容过滤和大小限制
* 支持图片的 Base64 编码存储
* 可自定义日志文件和图片保存路径
* 提供友好的控制台预览功能

配置说明
--------

程序的配置文件为 ``config.json``，支持以下配置项：

* 常规设置
    - 基础目录路径
    - 图片保存目录
    - 检查间隔时间
    - 最大日志文件数

* 内容类型设置
    - 是否启用文本内容
    - 是否启用图片内容
    - 是否启用文件路径
    - 最大文本长度
    - 最大图片大小

* 日志设置
    - 是否保存图片文件
    - 是否保存图片 Base64
    - 最大记录数量
    - JSON 格式化选项

* 显示设置
    - 是否显示预览
    - 是否显示时间戳
    - 控制台宽度
    - 最大预览长度

索引和搜索
----------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` 