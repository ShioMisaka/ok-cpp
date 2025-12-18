# ok-cpp

A lightweight C++ playground & template manager for Linux (CMake-based).

`ok-cpp` is designed to help you quickly create, build, run, and debug
small C++ projects using CMake.  
It is especially useful for learning C++, testing demos, and managing
multiple small example projects.

---

## Features

- 🚀 One-command build & run for CMake projects
- 📁 Project generator (`mkp`) with templates
- 🧩 Template system (default / Qt, extensible)
- 🧪 Debug & Release modes
- 🩺 Environment check with `doctor`
- 📦 User-level and system-level installation

---

## Installation

Before installing, make scripts executable:

```bash
chmod +x ./install.sh
chmod +x ./uninstall.sh
```

## System-wide installation
```bash
sudo ./install.sh
```

This installs `ok-cpp` into `/usr/local`.

## User-level installation (no sudo)
```bash
PREFIX=$HOME/.local ./install.sh
```

Make sure `~/.local/bin` is in your `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

You may want to add this line to `~/.bashrc` or `~/.zshrc`.

## Uninstall
```bash
./uninstall.sh
```

If installed with a custom prefix:

```bash
PREFIX=$HOME/.local ./uninstall.sh
```

## Usage
### Build & Run

```bash
ok-cpp run                  # Run project in current directory
ok-cpp run path/project     # Run project by path
ok-cpp run project_name     # Run project by name (search)
```

### Run Options

```bash
ok-cpp run -d
ok-cpp run --debug          # Debug mode (GDB)

ok-cpp run -c clang         # Use clang / clang++
ok-cpp run -c gun           # Use gcc / g++

ok-cpp run -p my_project    # Override project name
```

### Project Creation (mkp)

#### Use default template
```bash
ok-cpp mkp demos/hello
```

#### Use Qt template
```bash
ok-cpp mkp demos/qt_app -t qt
```

#### List available templates
```bash
ok-cpp mkp --list
```

#### Directory name and project name differ
```bash
ok-cpp mkp demos/app -n my_app
```

### Environment Check

Check whether required tools and dependencies are installed:
```bash
ok-cpp doctor
```

This checks:
- C++ compilers (g++ / clang++)
- CMake
- Ninja (optional)
- GDB (for Debug mode)
- Qt (for Qt templates)

### Version
```bash
ok-cpp --version
```

### Project Structure

```txt
ok_cpp/
├── bin/
│   └── ok-cpp              # Installed entry point
├── lib/ok-cpp/
│   ├── modules/            # Command modules
│   ├── templates/          # Project templates
│   └── common.sh           # Shared utilities
├── install.sh              # Install script
├── uninstall.sh            # Uninstall script
├── VERSION                 # Version file
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.