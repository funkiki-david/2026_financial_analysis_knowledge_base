#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
SAVE_SCRIPT="$ROOT_DIR/scripts/kb_save.sh"
PROCESSED_DIR="$ROOT_DIR/90_Inbox/processed"

usage() {
  cat <<'EOF'
Usage:
  kb_promote.sh --from FILE --type TYPE --title TITLE [options]

Options:
  --from FILE        Source file to promote from Inbox or another draft location
  --type TYPE        Route key for destination directory
  --title TITLE      File title used for destination filename
  --ext EXT          File extension override; default uses source file extension
  --subdir PATH      Extra subdirectory under the routed directory
  --date YYYY-MM-DD  Override date prefix
  --keep-source      Keep the original file in place
  --dry-run          Print the destination path without writing or moving files
  --help             Show this help
EOF
}

FROM_FILE=""
TYPE=""
TITLE=""
EXT=""
SUBDIR=""
DATE_OVERRIDE=""
KEEP_SOURCE="false"
DRY_RUN="false"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)
      FROM_FILE="${2:-}"
      shift 2
      ;;
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
    --keep-source)
      KEEP_SOURCE="true"
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

if [[ -z "$FROM_FILE" || -z "$TYPE" || -z "$TITLE" ]]; then
  echo "--from, --type, and --title are required." >&2
  usage >&2
  exit 1
fi

if [[ ! -f "$FROM_FILE" ]]; then
  echo "Source file not found: $FROM_FILE" >&2
  exit 1
fi

if [[ -z "$EXT" ]]; then
  BASENAME="${FROM_FILE##*/}"
  if [[ "$BASENAME" == *.* ]]; then
    EXT="${BASENAME##*.}"
  else
    EXT="md"
  fi
fi

SAVE_ARGS=(--type "$TYPE" --title "$TITLE" --ext "$EXT")
if [[ -n "$SUBDIR" ]]; then
  SAVE_ARGS+=(--subdir "$SUBDIR")
fi
if [[ -n "$DATE_OVERRIDE" ]]; then
  SAVE_ARGS+=(--date "$DATE_OVERRIDE")
fi
if [[ "$DRY_RUN" == "true" ]]; then
  SAVE_ARGS+=(--dry-run)
  exec "$SAVE_SCRIPT" "${SAVE_ARGS[@]}"
fi

TARGET_FILE="$("$SAVE_SCRIPT" "${SAVE_ARGS[@]}" --from "$FROM_FILE")"

if [[ "$KEEP_SOURCE" == "true" ]]; then
  printf '%s\n' "$TARGET_FILE"
  exit 0
fi

mkdir -p "$PROCESSED_DIR"
SOURCE_NAME="${FROM_FILE##*/}"
ARCHIVE_TARGET="$PROCESSED_DIR/$SOURCE_NAME"
COUNTER=1
while [[ -e "$ARCHIVE_TARGET" ]]; do
  ARCHIVE_TARGET="$PROCESSED_DIR/${SOURCE_NAME%.*}_$(printf '%02d' "$COUNTER").${SOURCE_NAME##*.}"
  COUNTER=$((COUNTER + 1))
done

mv "$FROM_FILE" "$ARCHIVE_TARGET"
printf '%s\n' "$TARGET_FILE"
