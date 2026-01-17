# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ok-cpp is a lightweight C++ playground and template manager for Linux using CMake. It provides a CLI tool to quickly create, build, run, and debug small C++ projects.

**The project is implemented in Python 3.8+** (previously bash).

## Installation & Testing

**Install Python dependencies first:**
```bash
pip install rich typer
```

Install to system:
```bash
sudo ./install.sh
```

Install to user directory (no sudo):
```bash
PREFIX=$HOME/.local ./install.sh
```

Test the installation:
```bash
ok-cpp --version
ok-cpp doctor
```

## Architecture

The project is a Python-based CLI tool with the following structure:

```
lib/okcpp/              # Python package
├── __init__.py
├── cli/                # CLI command modules
│   ├── __init__.py     # Command dispatcher
│   ├── run.py          # run command
│   ├── mkp.py          # mkp command
│   ├── doctor.py       # doctor command
│   └── config.py       # config command
├── core/               # Core business logic
│   ├── builder.py      # CMake build logic
│   ├── template.py     # Template processing
│   └── detector.py     # Environment detection
├── utils/              # Utility modules
│   ├── log.py          # Colored logging (rich)
│   ├── path.py         # Path handling
│   └── config.py       # User config management
└── templates/          # Project templates (default, qt)
```

- `bin/ok-cpp.py` - Python entry point (shebang script)
- `install.sh` - Installs Python package and dependencies
- `pyproject.toml` - Python project configuration

### Command Flow

1. `bin/ok-cpp` (Python script) receives a command
2. Commands support short aliases: r→run, m→mkp, d→doctor, c→config
3. The dispatcher (`cli/__init__.py:main()`) routes to the appropriate command module
4. Each command module imports from `core/` and `utils/` as needed

### Dependencies

- `rich` - Terminal colors and formatted output
- `typer` - CLI framework (optional, currently using manual arg parsing)

### Template System

Templates are stored in `lib/okcpp/templates/`. Each template must contain:
- `CMakeLists.txt` - Required, must have a `project(...)` line
- Source files (main.cpp, include/, src/, etc.)

When creating a project, `core/template.py:create_project()` copies the template directory and uses regex to replace the project name in CMakeLists.txt.

### CMake Project Detection

The `run` command detects the project name by:
1. First parsing `project(...)` from CMakeLists.txt via `core/builder.py:get_cmake_project_name()`
2. Falling back to directory name if not found

### Build System

- **Gun compiler**: Uses gcc/g++, generates "Unix Makefiles"
- **Clang compiler**: Uses clang/clang++, generates "Ninja"
- Build artifacts go to `build/` subdirectory within the project
- Compiler/build type changes trigger automatic `build/` cleanup

The build process in `core/builder.py:build_and_run()`:
1. Sets compiler environment variables (CC/CXX)
2. Detects project name
3. Checks if build cache needs cleaning
4. Runs CMake configure
5. Runs CMake build
6. Executes the binary (or GDB for Debug mode)

### Configuration

User config is stored in `${XDG_CONFIG_HOME:-$HOME/.config}/ok-cpp/config`:
- `COMPILER` - Default compiler (clang | gun)
- `TEMPLATE_NAME` - Default template for `mkp`

Config is managed by `utils/config.py:Config` class, which maintains compatibility with the original shell script format (KEY=value).

## Adding a New Template

1. Create a new directory under `lib/okcpp/templates/your_template/`
2. Add a `CMakeLists.txt` with a `project(...)` line
3. Add source files as needed
4. Template will be automatically discovered by `mkp --list`

## Development

**Run from source without installing:**
```bash
export PYTHONPATH=/path/to/ok-cpp/lib:$PYTHONPATH
./bin/ok-cpp.py <command>
```

**Or directly:**
```bash
./bin/ok-cpp.py <command>
```

## Template CMakeLists.txt Conventions

Templates should follow this pattern:
- Set `PROJECT_ROOT_DIR` to `${CMAKE_CURRENT_LIST_DIR}` for reference in source code
- Use `CMAKE_RUNTIME_OUTPUT_DIRECTORY` to place binaries in `build/`
- Support `CMAKE_BUILD_TYPE` (Debug/Release)
- Debug mode: `-g -O0`, defines `DEBUG_MODE`
- Release mode: `-O3`
- Mark sections with `# <<< Import SDK Package <<<` and `# >>> Import SDK Package >>>` for external deps

## Migration Notes (Shell → Python)

- All shell scripts in `lib/ok-cpp/` have been replaced by Python modules
- Configuration file format remains compatible (KEY=value)
- Command-line interface is identical
- Output format and colors match the original implementation
