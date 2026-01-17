"""Template handling for ok-cpp."""

import re
import shutil
from pathlib import Path
from typing import List

from okcpp.utils.log import die, info, print_blue, print_green_b, print_yellow_b


def list_templates(templates_dir: Path) -> List[str]:
    """列出所有可用的模板。

    Args:
        templates_dir: 模板目录

    Returns:
        模板名称列表
    """
    templates = []
    if not templates_dir.exists():
        return templates

    for item in templates_dir.iterdir():
        if item.is_dir() and (item / "CMakeLists.txt").exists():
            templates.append(item.name)

    return sorted(templates)


def create_project(
    target_path: str,
    template_name: str,
    project_name: str,
    templates_dir: Path,
) -> Path:
    """从模板创建项目。

    Args:
        target_path: 目标路径（可以是相对或绝对路径）
        template_name: 模板名称
        project_name: 项目名称（用于 CMake project()）
        templates_dir: 模板根目录

    Returns:
        创建的项目目录的绝对路径
    """
    # 解析目标路径
    target_dir = Path(target_path)
    if not target_dir.is_absolute():
        target_dir = Path.cwd() / target_dir

    # 检查目标是否已存在
    if target_dir.exists():
        die(f"目标已存在: {target_dir}")

    # 检查模板是否存在
    template_dir = templates_dir / template_name
    if not template_dir.exists():
        die(f"模板不存在: {template_name}")
    if not (template_dir / "CMakeLists.txt").exists():
        die(f"模板缺少 CMakeLists.txt: {template_name}")

    # 如果没有指定项目名，使用目录名
    if not project_name:
        project_name = target_dir.name

    # 创建父目录
    target_dir.parent.mkdir(parents=True, exist_ok=True)

    # 复制模板目录
    shutil.copytree(template_dir, target_dir)

    # 替换 CMakeLists.txt 中的项目名
    cmake_file = target_dir / "CMakeLists.txt"
    _replace_cmake_project_name(cmake_file, project_name)

    print()
    print_green_b(f"已创建项目: {target_dir}")
    print_yellow_b(f"Template: {template_name}")
    print_blue(f"CMake project name: {project_name}")
    info(f"下一步: cd {target_dir} && ok-cpp run 来编译运行")

    return target_dir


def _replace_cmake_project_name(cmake_file: Path, new_project_name: str) -> None:
    """替换 CMakeLists.txt 中的项目名称。

    Args:
        cmake_file: CMakeLists.txt 文件路径
        new_project_name: 新的项目名称
    """
    try:
        content = cmake_file.read_text(encoding="utf-8")
        # 替换 project(...) 中的名称
        # 支持: project(foo), project(foo LANGUAGES CXX), project(foo VERSION 1.0)
        new_content = re.sub(
            r"(^\s*project\s*\(\s*)([A-Za-z0-9_-]+)",
            rf"\1{new_project_name}",
            content,
            flags=re.MULTILINE | re.IGNORECASE,
        )
        cmake_file.write_text(new_content, encoding="utf-8")
    except Exception as e:
        die(f"无法更新 CMakeLists.txt: {e}")


def get_template_info(templates_dir: Path, template_name: str) -> dict:
    """获取模板信息。

    Args:
        templates_dir: 模板根目录
        template_name: 模板名称

    Returns:
        包含模板信息的字典
    """
    template_dir = templates_dir / template_name

    if not template_dir.exists():
        return {"exists": False}

    cmake_file = template_dir / "CMakeLists.txt"
    project_name = None

    if cmake_file.exists():
        # 尝试读取项目名
        try:
            import re

            content = cmake_file.read_text(encoding="utf-8")
            match = re.search(
                r"^\s*project\s*\(\s*([A-Za-z0-9_-]+)",
                content,
                re.MULTILINE | re.IGNORECASE,
            )
            if match:
                project_name = match.group(1)
        except Exception:
            pass

    return {
        "exists": True,
        "has_cmake": cmake_file.exists(),
        "project_name": project_name,
        "path": template_dir,
    }
