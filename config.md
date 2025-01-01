# 配置文件说明

配置文件 `config.json` 包含了程序的所有可配置选项。以下是各配置项的详细说明：

## 常规设置 (general)

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| check_interval | float | 1.0 | 检查剪贴板的时间间隔（秒） |
| max_log_files | int | 30 | 保留的日志文件最大数量 |
| base_dir | string | "logs" | 日志根目录 |
| images_dir | string | "images" | 图片存储目录名 |

## 日志设置 (logging)

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| save_image_file | bool | true | 是否保存图片物理文件 |
| save_image_base64 | bool | true | 是否在日志中保存base64数据 |
| max_entries_per_file | int | 1000 | 每个日志文件最大记录数 |
| indent_json | bool | true | 是否格式化JSON输出 |

## 内容类型设置 (content_types)

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| enable_text | bool | true | 是否记录文本内容 |
| enable_image | bool | true | 是否记录图片内容 |
| enable_files | bool | true | 是否记录文件路径 |
| max_text_length | int | 1000000 | 最大文本长度（字符） |
| max_image_size | int | 10485760 | 最大图片大小（字节，约10MB） |

## 显示设置 (display)

| 配置项 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| show_content_preview | bool | true | 是否在控制台显示内容预览 |
| max_preview_length | int | 200 | 预览内容的最大长度 |
| show_timestamps | bool | true | 是否显示时间戳 |
| console_width | int | 80 | 控制台输出宽度 |

## 使用说明

1. 所有配置项都有默认值，你可以只修改需要改变的选项
2. 修改配置文件后需要重启程序才能生效
3. 如果配置文件不存在或格式错误，程序会使用默认值
4. 建议在修改配置文件之前先备份

## 配置示例

```json
{
    "general": {
        "check_interval": 0.5,    // 更频繁地检查
        "max_log_files": 7        // 只保留一周的日志
    },
    "logging": {
        "save_image_base64": false  // 不在日志中保存base64数据
    }
}
```

注意：实际的 JSON 文件中不能包含注释，上面的示例仅用于说明。 