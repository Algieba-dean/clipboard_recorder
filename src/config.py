"""配置管理模块

此模块负责加载和管理程序的配置信息，支持从配置文件读取和合并默认配置。

Classes:
    Config: 配置管理类，处理配置的加载和访问
"""
import json
import os
from typing import Dict, Any
from .constants import Paths, DefaultConfig, Messages

class Config:
    """配置管理类，负责加载和管理配置。
    
    此类处理配置文件的加载、默认配置的合并，并提供统一的配置访问接口。
    支持多层级的配置结构，可以通过section和key来访问具体的配置项。

    Attributes:
        config_file (str): 配置文件的路径
        _settings (Dict): 当前生效的配置数据
    """

    def __init__(self, config_file: str = Paths.DEFAULT_CONFIG_FILE):
        """初始化配置管理器。

        Args:
            config_file (str, optional): 配置文件路径。默认为constants.Paths.DEFAULT_CONFIG_FILE
        """
        self.config_file = config_file
        self._settings = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件。

        尝试从指定的配置文件加载用户配置，如果失败则使用默认配置。
        配置文件应该是一个有效的JSON文件。

        Returns:
            Dict[str, Any]: 合并后的配置字典
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    return self._merge_config(DefaultConfig.DEFAULT_CONFIG, user_config)
        except Exception as e:
            print(Messages.Error.CONFIG_LOAD_ERROR.format(str(e)))
            print(Messages.Error.USE_DEFAULT_CONFIG)
        return DefaultConfig.DEFAULT_CONFIG.copy()

    def _merge_config(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """递归合并配置字典。

        将用户配置与默认配置进行深度合并，保留用户配置中的值。

        Args:
            default (Dict[str, Any]): 默认配置字典
            user (Dict[str, Any]): 用户配置字典

        Returns:
            Dict[str, Any]: 合并后的配置字典
        """
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result

    def get(self, section: str, key: str) -> Any:
        """获取指定的配置值。

        Args:
            section (str): 配置的区段名称
            key (str): 配置项的键名

        Returns:
            Any: 配置值，如果未找到则返回默认配置中的值
        """
        return self._settings.get(section, {}).get(key, DefaultConfig.DEFAULT_CONFIG[section][key]) 