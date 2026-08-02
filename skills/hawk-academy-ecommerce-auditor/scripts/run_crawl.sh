#!/usr/bin/env bash
#
# run_crawl.sh - SiteOne crawl wrapper for the Hawk Academy eCommerce Auditor.
#
# Usage:
#   bash run_crawl.sh <store-url> <out-dir> [max-depth] [extra crawler flags...]
#
# Example:
#   bash run_crawl.sh "https://store.example.com" "./audit/crawl" 3
#   bash run_crawl.sh "https://store.example.com" "./audit/crawl" 3 --max-visited-urls=400
#
# Produces, inside <out-dir>:
#   offline/     mirrored HTML export (what analyze_ecommerce.py reads)
#   crawl.json   JSON inventory of every URL crawled
#   report.html  the crawler's own interactive report
#   robots.txt   copied out of the export when the crawler saved it
#
# Works on macOS (Apple Silicon + Intel), Linux, and Windows via Git Bash.
# There is no Homebrew dependency. The crawler is located in this order:
#   1. $SITEONE_CRAWLER (explicit override)
#   2. siteone-crawler already on PATH
#   3. a previous install in ~/siteone-crawler or C:\siteone-crawler
#   4. the bundled binary shipped with the sibling `site-crawler` skill
#   5. a download from the SiteOne GitHub release
# Windows users without Git Bash should use run_crawl.ps1 instead.

set -euo pipefail

CRAWLER_VERSION="v2.3.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- args --------------------------------------------------------------------

if [ $# -lt 2 ]; then
  echo "Usage: bash run_crawl.sh <store-url> <out-dir> [max-depth] [extra crawler flags...]" >&2
  exit 2
fi

URL="$1"; shift
OUT_DIR="$1"; shift
MAX_DEPTH="${1:-3}"
if [ $# -gt 0 ]; then
  case "$1" in
    --*) : ;;          # first extra arg is a flag, so depth stays at its default
    *) shift ;;        # it was the depth, consume it
  esac
fi
EXTRA=("$@")

case "$URL" in
  http://*|https://*) : ;;
  *) echo "ERROR: store URL must start with http:// or https:// (got: $URL)" >&2; exit 2 ;;
esac

mkdir -p "$OUT_DIR"
OUT_DIR="$(cd "$OUT_DIR" && pwd)"

# --- platform ----------------------------------------------------------------

detect_platform() {
  local os arch
  os="$(uname -s 2>/dev/null || echo unknown)"
  arch="$(uname -m 2>/dev/null || echo unknown)"
  case "$os" in
    Darwin)
      if [ "$arch" = "arm64" ]; then echo "macos-arm64"; else echo "macos-x64"; fi ;;
    Linux)
      case "$arch" in
        aarch64|arm64) echo "linux-arm64" ;;
        *) echo "linux-x64" ;;
      esac ;;
    MINGW*|MSYS*|CYGWIN*|Windows_NT) echo "win-x64" ;;
    *) echo "unknown" ;;
  esac
}

PLATFORM="$(detect_platform)"
IS_WINDOWS=0
[ "$PLATFORM" = "win-x64" ] && IS_WINDOWS=1

package_name() {
  case "$1" in
    macos-arm64) echo "siteone-crawler-${CRAWLER_VERSION}-macos-arm64.tar.gz" ;;
    macos-x64)   echo "siteone-crawler-${CRAWLER_VERSION}-macos-x64.tar.gz" ;;
    linux-arm64) echo "siteone-crawler-${CRAWLER_VERSION}-linux-arm64.tar.gz" ;;
    linux-x64)   echo "siteone-crawler-${CRAWLER_VERSION}-linux-x64.tar.gz" ;;
    win-x64)     echo "siteone-crawler-${CRAWLER_VERSION}-win-x64.zip" ;;
    *) return 1 ;;
  esac
}

# Git Bash mangles unix-style paths passed to native .exe binaries. Convert
# them ourselves and switch the automatic conversion off.
to_native() {
  if [ "$IS_WINDOWS" -eq 1 ] && command -v cygpath >/dev/null 2>&1; then
    cygpath -w "$1"
  else
    echo "$1"
  fi
}

# --- locate an existing crawler ----------------------------------------------

find_crawler() {
  if [ -n "${SITEONE_CRAWLER:-}" ] && [ -f "$SITEONE_CRAWLER" ]; then
    echo "$SITEONE_CRAWLER"; return 0
  fi
  local name
  for name in siteone-crawler siteone-crawler.exe; do
    if command -v "$name" >/dev/null 2>&1; then
      command -v "$name"; return 0
    fi
  done
  local cand
  for cand in \
    "$HOME/siteone-crawler/siteone-crawler" \
    "$HOME/siteone-crawler/siteone-crawler.exe" \
    "$HOME/.local/siteone-crawler/siteone-crawler" \
    "/c/siteone-crawler/siteone-crawler.exe" \
    "/mnt/c/siteone-crawler/siteone-crawler.exe"; do
    if [ -f "$cand" ]; then echo "$cand"; return 0; fi
  done
  return 1
}

# --- find the binary bundled with the sibling site-crawler skill --------------

find_bundled_package() {
  local pkg root found
  pkg="$(package_name "$PLATFORM")" || return 1

  # The site-crawler skill ships macOS and Windows builds under binaries/.
  # Look next to this skill first, then in the usual plugin/skill locations.
  local roots=(
    "$SCRIPT_DIR/.."
    "$SCRIPT_DIR/../.."
    "$SCRIPT_DIR/../../.."
    "$HOME/.claude/plugins/cache"
    "$HOME/.claude/skills"
    "$HOME/.claude/plugins"
  )
  for root in "${roots[@]}"; do
    [ -d "$root" ] || continue
    found="$(find "$root" -maxdepth 7 -type f -name "$pkg" 2>/dev/null | head -1)"
    if [ -n "$found" ]; then echo "$found"; return 0; fi
  done
  return 1
}

# --- install -----------------------------------------------------------------

install_crawler() {
  local dest="$HOME/siteone-crawler"
  local pkg archive tmp
  pkg="$(package_name "$PLATFORM")" || {
    echo "ERROR: unsupported platform ($(uname -s 2>/dev/null) $(uname -m 2>/dev/null))." >&2
    echo "Install SiteOne Crawler manually: https://github.com/janreges/siteone-crawler/releases" >&2
    return 1
  }

  mkdir -p "$dest"
  tmp="$(mktemp -d)"

  if archive="$(find_bundled_package)"; then
    echo "-> Installing SiteOne Crawler from the bundled site-crawler binary (no download needed)." >&2
    echo "   $archive" >&2
  else
    echo "-> No bundled binary for $PLATFORM. Downloading the official release..." >&2
    archive="$tmp/$pkg"
    local url="https://github.com/janreges/siteone-crawler/releases/download/${CRAWLER_VERSION}/${pkg}"
    if command -v curl >/dev/null 2>&1; then
      curl -fsSL "$url" -o "$archive" || { echo "ERROR: download failed: $url" >&2; return 1; }
    elif command -v wget >/dev/null 2>&1; then
      wget -q "$url" -O "$archive" || { echo "ERROR: download failed: $url" >&2; return 1; }
    else
      echo "ERROR: neither curl nor wget is available to download the crawler." >&2
      echo "Download it manually and set SITEONE_CRAWLER to the binary path:" >&2
      echo "  $url" >&2
      return 1
    fi
  fi

  case "$archive" in
    *.tar.gz)
      tar -xzf "$archive" -C "$dest" --strip-components=1 ;;
    *.zip)
      if command -v unzip >/dev/null 2>&1; then
        unzip -q -o "$archive" -d "$tmp/x"
      elif command -v powershell.exe >/dev/null 2>&1; then
        powershell.exe -NoProfile -Command \
          "Expand-Archive -Path '$(to_native "$archive")' -DestinationPath '$(to_native "$tmp/x")' -Force" >/dev/null
      else
        echo "ERROR: no unzip available to extract $archive" >&2; return 1
      fi
      # Archives contain a single top-level siteone-crawler/ directory.
      if [ -d "$tmp/x/siteone-crawler" ]; then
        cp -R "$tmp/x/siteone-crawler/." "$dest/"
      else
        cp -R "$tmp/x/." "$dest/"
      fi ;;
    *)
      echo "ERROR: unrecognised archive format: $archive" >&2; return 1 ;;
  esac

  rm -rf "$tmp"
  chmod +x "$dest/siteone-crawler" 2>/dev/null || true

  if [ -f "$dest/siteone-crawler.exe" ]; then
    echo "$dest/siteone-crawler.exe"; return 0
  elif [ -f "$dest/siteone-crawler" ]; then
    echo "$dest/siteone-crawler"; return 0
  fi
  echo "ERROR: install completed but no crawler binary found in $dest" >&2
  return 1
}

# --- resolve the crawler ------------------------------------------------------

echo "-> Platform detected: $PLATFORM"

if CRAWLER="$(find_crawler)"; then
  echo "-> Using SiteOne Crawler at: $CRAWLER"
else
  echo "-> SiteOne Crawler not found. Installing it now (free, no licence or signup)."
  # install_crawler sends all chatter to stderr and only the binary path to stdout.
  CRAWLER="$(install_crawler)" || exit 1
  if [ -z "$CRAWLER" ] || [ ! -f "$CRAWLER" ]; then
    echo "ERROR: could not install SiteOne Crawler automatically." >&2
    echo "Install it manually, then set SITEONE_CRAWLER to the binary path and re-run:" >&2
    echo "  https://github.com/janreges/siteone-crawler/releases/tag/${CRAWLER_VERSION}" >&2
    exit 1
  fi
  echo "-> Installed to: $CRAWLER"
fi

# --- crawl -------------------------------------------------------------------

export MSYS2_ARG_CONV_EXCL='*'

OFFLINE_DIR="$OUT_DIR/offline"
JSON_FILE="$OUT_DIR/crawl.json"
HTML_REPORT="$OUT_DIR/report.html"

echo "-> Crawling $URL (max depth $MAX_DEPTH)..."
echo "   Output: $OUT_DIR"

set +e
"$CRAWLER" \
  --url="$URL" \
  --max-depth="$MAX_DEPTH" \
  --offline-export-dir="$(to_native "$OFFLINE_DIR")" \
  --offline-export-preserve-url-structure \
  --offline-export-no-auto-redirect-html \
  --offline-export-remove-unwanted-code=0 \
  --output-json-file="$(to_native "$JSON_FILE")" \
  --output-html-report="$(to_native "$HTML_REPORT")" \
  "${EXTRA[@]+"${EXTRA[@]}"}"
CRAWL_STATUS=$?
set -e

if [ ! -d "$OFFLINE_DIR" ]; then
  echo "ERROR: the crawl produced no offline export at $OFFLINE_DIR (exit $CRAWL_STATUS)." >&2
  echo "The site may block crawlers, or the URL may be wrong. Try a lower --max-depth," >&2
  echo "or check the URL in a browser first." >&2
  exit 1
fi

if [ "$CRAWL_STATUS" -ne 0 ]; then
  echo "WARNING: crawler exited with status $CRAWL_STATUS but an export was produced."
  echo "Continuing with what it captured - note the limitation in the audit."
fi

# --- robots.txt ---------------------------------------------------------------
# The offline export keeps robots.txt when the crawler fetched it. When it did
# not, the skill fetches it with web_fetch instead (see SKILL.md Step 2).

ROBOTS_SRC="$(find "$OFFLINE_DIR" -maxdepth 3 -type f -name 'robots.txt' 2>/dev/null | head -1)"
if [ -n "$ROBOTS_SRC" ]; then
  cp "$ROBOTS_SRC" "$OUT_DIR/robots.txt"
  echo "-> robots.txt saved to $OUT_DIR/robots.txt"
else
  echo "ROBOTS_MISSING: robots.txt was not in the crawl."
  echo "Fetch ${URL%/}/robots.txt with the web_fetch tool and save it to $OUT_DIR/robots.txt"
  echo "before running analyze_ecommerce.py. Do not use curl or wget for this."
fi

PAGE_COUNT="$(find "$OFFLINE_DIR" -type f \( -name '*.html' -o -name '*.htm' \) 2>/dev/null | wc -l | tr -d ' ')"

echo ""
echo "Crawl complete."
echo "  HTML pages exported : $PAGE_COUNT"
echo "  Offline export      : $OFFLINE_DIR"
echo "  JSON inventory      : $JSON_FILE"
echo "  HTML report         : $HTML_REPORT"
echo ""
echo "Next: python3 scripts/analyze_ecommerce.py --crawl-dir \"$OUT_DIR\" --base-url \"$URL\" --out \"<work-dir>/findings.json\""
