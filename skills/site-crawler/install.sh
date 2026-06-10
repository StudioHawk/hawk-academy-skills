#!/bin/bash
# SiteOne Crawler — one-command installer (Mac + Linux)
# Usage:  bash install.sh
# Installs the bundled binary to ~/siteone-crawler and adds a `siteone-crawler` command.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
DEST="$HOME/siteone-crawler"
OS="$(uname -s)"; ARCH="$(uname -m)"

echo "→ Detecting your computer..."
if [ "$OS" = "Darwin" ]; then
  if [ "$ARCH" = "arm64" ]; then PKG="siteone-crawler-v2.3.0-macos-arm64.tar.gz"; LABEL="Mac (Apple Silicon)";
  else PKG="siteone-crawler-v2.3.0-macos-x64.tar.gz"; LABEL="Mac (Intel)"; fi
elif [ "$OS" = "Linux" ]; then
  if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then URLPKG="siteone-crawler-v2.3.0-linux-arm64.tar.gz";
  else URLPKG="siteone-crawler-v2.3.0-linux-x64.tar.gz"; fi
  LABEL="Linux"; PKG=""
else
  echo "Windows detected? Use the win-x64 zip in binaries/ instead — see README."; exit 1
fi
echo "   $LABEL"

mkdir -p "$DEST"
if [ -n "$PKG" ] && [ -f "$HERE/binaries/$PKG" ]; then
  echo "→ Installing from bundled package (no internet needed)..."
  tar -xzf "$HERE/binaries/$PKG" -C "$DEST" --strip-components=1
else
  echo "→ Downloading Linux build from GitHub..."
  curl -sL "https://github.com/janreges/siteone-crawler/releases/download/v2.3.0/$URLPKG" | tar -xz -C "$DEST" --strip-components=1
fi
chmod +x "$DEST/siteone-crawler"

# add to PATH via symlink if possible, else profile
BIN_LINK="/usr/local/bin/siteone-crawler"
if ln -sf "$DEST/siteone-crawler" "$BIN_LINK" 2>/dev/null; then
  echo "→ Command installed: siteone-crawler"
else
  SHELL_RC="$HOME/.zshrc"; [ -n "$BASH_VERSION" ] && SHELL_RC="$HOME/.bashrc"
  grep -q 'siteone-crawler' "$SHELL_RC" 2>/dev/null || echo "export PATH=\"\$PATH:$DEST\"" >> "$SHELL_RC"
  echo "→ Added to PATH in $SHELL_RC (open a new terminal, or run: source $SHELL_RC)"
fi

echo ""
echo "✅ Done! Crawl your site with:"
echo "   siteone-crawler --url=https://yourdomain.com.au/"
echo ""
echo "Results (HTML report + files) land in: $DEST/tmp"
