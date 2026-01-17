"""Configuration file management."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from okcpp.cli import ROOT_DIR


@dataclass
class Config:
    """ok-cpp 用户配置。

    配置文件位置: ${XDG_CONFIG_HOME:-$HOME/.config}/ok-cpp/config
    格式: 简单的 KEY=value 格式，与原版 shell 脚本兼容
    """

    compiler: str = "gun"
    template_name: str = "default"

    # 内部字段
    _config_dir: Path = field(init=False, repr=False)
    _config_file: Path = field(init=False, repr=False)

    def __post_init__(self):
        """初始化配置路径。"""
        config_base = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        self._config_dir = Path(config_base) / "ok-cpp"
        self._config_file = self._config_dir / "config"

    def load(self) -> None:
        """从配置文件加载配置。

        如果配置文件不存在，保持默认值。
        """
        if not self._config_file.exists():
            return

        try:
            content = self._config_file.read_text(encoding="utf-8")
            for line in content.splitlines():
                line = line.strip()
                # 跳过空行和注释
                if not line or line.startswith("#"):
                    continue
                # 解析 KEY=value
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    if key == "COMPILER":
                        self.compiler = value
                    elif key == "TEMPLATE_NAME":
                        self.template_name = value
        except Exception:
            # 如果读取失败，静默失败，保持默认值
            pass

    def save(self) -> None:
        """保存配置到文件。"""
        self._config_dir.mkdir(parents=True, exist_ok=True)
        content = (
            "# ok-cpp user config (auto-generated)\n"
            "\n"
            f"COMPILER={self.compiler}\n"
            f"TEMPLATE_NAME={self.template_name}\n"
        )
        self._config_file.write_text(content, encoding="utf-8")

    @staticmethod
    def validate_compiler(compiler: str) -> bool:
        """验证编译器名称是否有效。

        Args:
            compiler: 编译器名称

        Returns:
            如果是有效的编译器名称返回 True
        """
        return compiler in ("clang", "gun")

    @staticmethod
    def validate_template(template_name: str, templates_dir: Optional[Path] = None) -> bool:
        """验证模板是否存在。

        Args:
            template_name: 模板名称
            templates_dir: 模板目录，默认使用 okcpp 的 templates 目录

        Returns:
            如果模板存在返回 True
        """
        if templates_dir is None:
            templates_dir = ROOT_DIR / "templates"
        return (templates_dir / template_name).exists() and (
            templates_dir / template_name / "CMakeLists.txt"
        ).exists()


# 全局配置实例
_global_config: Optional[Config] = None


def get_config() -> Config:
    """获取全局配置实例（单例模式）。

    Returns:
        Config 实例，会自动加载配置文件
    """
    global _global_config
    if _global_config is None:
        _global_config = Config()
        _global_config.load()
    return _global_config


def reset_config() -> None:
    """重置全局配置（用于测试或卸载）。"""
    global _global_config
    _global_config = None
