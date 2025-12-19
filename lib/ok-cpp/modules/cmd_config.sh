#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${OK_CPP_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
COMMON="$ROOT_DIR/lib/ok-cpp/common.sh"

# shellcheck source=/dev/null
source "$COMMON"

load_user_config

usage() {
    cat <<EOF
Usage:
  ok-cpp config show
  ok-cpp config set <key> <value>
  ok-cpp config reset

Config keys:
  compiler        default compiler for 'ok-cpp run'   (clang | gun)
  template        default template for 'ok-cpp mkp'

Examples:
  ok-cpp config show
  ok-cpp config set compiler clang
  ok-cpp config set template qt
  ok-cpp config reset
EOF
}

cmd="${1:-show}"
shift || true

case "$cmd" in
    show)
        echo "Config file: $OK_CPP_CONFIG_FILE"
        echo
        echo "COMPILER=${COMPILER:-gun}"
        echo "TEMPLATE_NAME=${TEMPLATE_NAME:-default}"
        ;;

    set)
        [[ $# -eq 2 ]] || die "Usage: ok-cpp config set <key> <value>"

        key="$1"
        value="$2"

        case "$key" in
            compiler)
                validate_compiler "$value" \
                    || die "Invalid compiler: $value (clang | gun)"
                COMPILER="$value"
                ;;
            template)
                validate_template "$value" \
                    || die "Template not found: $value"
                TEMPLATE_NAME="$value"
                ;;
            *)
                die "Unknown config key: $key"
                ;;
        esac

        write_user_config
        info "Config updated: $key=$value"
        ;;

    reset)
        rm -f "$OK_CPP_CONFIG_FILE"
        info "Config reset (using defaults)"
        ;;

    -h|--help|help)
        usage
        ;;

    *)
        die "Unknown config command: $cmd"
        ;;
esac
