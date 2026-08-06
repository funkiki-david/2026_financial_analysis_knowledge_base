#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$ROOT_DIR/config/kb.env"

if [[ -f "$CONFIG_FILE" ]]; then
  # shellcheck source=/dev/null
  source "$CONFIG_FILE"
fi

KB_ROOT="${KB_ROOT:-$ROOT_DIR}"
KB_DATE_MODE="${KB_DATE_MODE:-today}"
KB_FORCE_DATE="${KB_FORCE_DATE:-}"
KB_TIMEZONE="${KB_TIMEZONE:-America/Los_Angeles}"
KB_LOG_FILE="${KB_LOG_FILE:-$KB_ROOT/logs/save.log}"

usage() {
  cat <<'EOF'
Usage:
  kb_save.sh --type TYPE --title TITLE [options]

Options:
  --type TYPE        Route key for destination directory
  --title TITLE      File title used for filename generation
  --ext EXT          File extension, default: md
  --subdir PATH      Extra subdirectory under the routed directory
  --date YYYY-MM-DD  Override date prefix
  --from FILE        Read content from an existing file
  --content TEXT     Read content from a literal string
  --dry-run          Print the target path without writing a file
  --help             Show this help

Input:
  If neither --from nor --content is provided, the script reads from stdin.
EOF
}

TYPE=""
TITLE=""
EXT="md"
SUBDIR=""
DATE_OVERRIDE=""
FROM_FILE=""
INLINE_CONTENT=""
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
    --content)
      INLINE_CONTENT="${2:-}"
      shift 2
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

route_dir() {
  case "$1" in
    project) echo "00_Project/docs" ;;
    foundation) echo "01_Financial_Foundations" ;;
    market) echo "02_Market_Structure" ;;
    framework) echo "03_Research_Frameworks" ;;
    company) echo "04_Company_Notes/Active_Research" ;;
    watchlist) echo "04_Company_Notes/Watchlist" ;;
    review-daily) echo "05_Market_Reviews/Daily" ;;
    review-weekly) echo "05_Market_Reviews/Weekly" ;;
    review-monthly) echo "05_Market_Reviews/Monthly" ;;
    review-annual) echo "05_Market_Reviews/Annual" ;;
    template) echo "06_Research_Templates" ;;
    ai-workflow) echo "07_AI_Workflows/Research_Workflows" ;;
    prompt) echo "07_AI_Workflows/Prompt_Library" ;;
    source) echo "08_Data_and_Sources/references" ;;
    data-raw) echo "08_Data_and_Sources/raw_data" ;;
    data-processed) echo "08_Data_and_Sources/processed_data" ;;
    learning) echo "09_Learning_Log" ;;
    glossary) echo "10_Glossary" ;;
    inbox) echo "90_Inbox/incoming" ;;
    *)
      echo "Unsupported type: $1" >&2
      exit 1
      ;;
  esac
}

slugify() {
  printf '%s' "$1" \
    | sed -E 's#[/:*?"<>|\\]+#_#g; s/[[:space:]]+/_/g; s/_+/_/g; s/^_+|_+$//g'
}

safe_subdir() {
  printf '%s' "$1" \
    | sed -E 's#^\./##; s#/\.\.?(/|$)#/#g; s#^/##'
}

DATE_PREFIX=""
if [[ -n "$DATE_OVERRIDE" ]]; then
  DATE_PREFIX="$DATE_OVERRIDE"
elif [[ -n "$KB_FORCE_DATE" ]]; then
  DATE_PREFIX="$KB_FORCE_DATE"
elif [[ "$KB_DATE_MODE" == "today" ]]; then
  DATE_PREFIX="$(TZ="$KB_TIMEZONE" date '+%Y-%m-%d')"
fi

ROUTE="$(route_dir "$TYPE")"
SUBDIR_CLEAN="$(safe_subdir "$SUBDIR")"
DEST_DIR="$KB_ROOT/$ROUTE"
if [[ -n "$SUBDIR_CLEAN" ]]; then
  DEST_DIR="$DEST_DIR/$SUBDIR_CLEAN"
fi
mkdir -p "$DEST_DIR" "$(dirname "$KB_LOG_FILE")"

TITLE_SLUG="$(slugify "$TITLE")"
if [[ -z "$TITLE_SLUG" ]]; then
  echo "Title produced an empty filename. Please use a more descriptive title." >&2
  exit 1
fi

BASE_NAME="$TITLE_SLUG"
if [[ -n "$DATE_PREFIX" ]]; then
  BASE_NAME="${DATE_PREFIX}_${BASE_NAME}"
fi

TARGET_FILE="$DEST_DIR/$BASE_NAME.$EXT"
COUNTER=1
while [[ -e "$TARGET_FILE" ]]; do
  TARGET_FILE="$DEST_DIR/${BASE_NAME}_$(printf '%02d' "$COUNTER").$EXT"
  COUNTER=$((COUNTER + 1))
done

if [[ "$DRY_RUN" == "true" ]]; then
  printf '%s\n' "$TARGET_FILE"
  exit 0
fi

if [[ -n "$FROM_FILE" ]]; then
  cp "$FROM_FILE" "$TARGET_FILE"
elif [[ -n "$INLINE_CONTENT" ]]; then
  printf '%s\n' "$INLINE_CONTENT" > "$TARGET_FILE"
else
  cat > "$TARGET_FILE"
fi

printf '%s | type=%s | file=%s\n' "$(TZ="$KB_TIMEZONE" date '+%Y-%m-%d %H:%M:%S')" "$TYPE" "$TARGET_FILE" >> "$KB_LOG_FILE"
printf '%s\n' "$TARGET_FILE"
