#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SAVE_SCRIPT="$ROOT_DIR/scripts/kb_save.sh"

usage() {
  cat <<'EOF'
Usage:
  kb_capture.sh --type TYPE --title TITLE [options]

Options:
  --type TYPE        Route key for destination directory
  --title TITLE      File title used for filename generation
  --ext EXT          File extension, default: md
  --subdir PATH      Extra subdirectory under the routed directory
  --date YYYY-MM-DD  Override date prefix
  --from FILE        Read content from a file
  --text TEXT        Read content from inline text
  --clipboard        Read content from macOS clipboard
  --dry-run          Print the target path without writing a file
  --help             Show this help

Behavior:
  If no source option is provided, the script falls back to clipboard first,
  then stdin when clipboard is empty.
EOF
}

TYPE=""
TITLE=""
EXT="md"
SUBDIR=""
DATE_OVERRIDE=""
FROM_FILE=""
INLINE_TEXT=""
USE_CLIPBOARD="false"
DRY_RUN="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --type)
      TYPE="${2:-}"
      shift 2
      ;;
    --title)
      TITLE="${2:-}"
      shift 2
      ;;
    --ext)
      EXT="${2:-}"
      shift 2
      ;;
    --subdir)
      SUBDIR="${2:-}"
      shift 2
      ;;
    --date)
      DATE_OVERRIDE="${2:-}"
      shift 2
      ;;
    --from)
      FROM_FILE="${2:-}"
      shift 2
      ;;
    --text)
      INLINE_TEXT="${2:-}"
      shift 2
      ;;
    --clipboard)
      USE_CLIPBOARD="true"
      shift
      ;;
    --dry-run)
      DRY_RUN="true"
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$TYPE" || -z "$TITLE" ]]; then
  echo "--type and --title are required." >&2
  usage >&2
  exit 1
fi

COMMON_ARGS=(--type "$TYPE" --title "$TITLE" --ext "$EXT")
if [[ -n "$SUBDIR" ]]; then
  COMMON_ARGS+=(--subdir "$SUBDIR")
fi
if [[ -n "$DATE_OVERRIDE" ]]; then
  COMMON_ARGS+=(--date "$DATE_OVERRIDE")
fi
if [[ "$DRY_RUN" == "true" ]]; then
  COMMON_ARGS+=(--dry-run)
fi

if [[ -n "$FROM_FILE" ]]; then
  exec "$SAVE_SCRIPT" "${COMMON_ARGS[@]}" --from "$FROM_FILE"
fi

if [[ -n "$INLINE_TEXT" ]]; then
  exec "$SAVE_SCRIPT" "${COMMON_ARGS[@]}" --content "$INLINE_TEXT"
fi

if [[ "$USE_CLIPBOARD" == "true" ]]; then
  if ! command -v pbpaste >/dev/null 2>&1; then
    echo "pbpaste is not available on this system." >&2
    exit 1
  fi

  CLIPBOARD_CONTENT="$(pbpaste)"
  if [[ -z "$CLIPBOARD_CONTENT" ]]; then
    echo "Clipboard is empty." >&2
    exit 1
  fi

  exec "$SAVE_SCRIPT" "${COMMON_ARGS[@]}" --content "$CLIPBOARD_CONTENT"
fi

if command -v pbpaste >/dev/null 2>&1; then
  CLIPBOARD_FALLBACK="$(pbpaste)"
  if [[ -n "$CLIPBOARD_FALLBACK" ]]; then
    exec "$SAVE_SCRIPT" "${COMMON_ARGS[@]}" --content "$CLIPBOARD_FALLBACK"
  fi
fi

exec "$SAVE_SCRIPT" "${COMMON_ARGS[@]}"
