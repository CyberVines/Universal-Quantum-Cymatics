#!/bin/bash
# ──────────────────────────────────────────────────────────────────────────────
# UQC — Universal Quantum Codec  |  macOS .app Bundle Builder
# Copyright 2026 Cyber Vines, LLC (cybervines.com)
#
# Usage:  ./build.sh [--dmg]
#   --dmg   Also create a distributable DMG disk image
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
UQC_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
APP_DIR="$SCRIPT_DIR/UQC.app"
CONTENTS="$APP_DIR/Contents"

echo "──────────────────────────────────────────"
echo "  UQC macOS .app Bundle Builder"
echo "──────────────────────────────────────────"
echo ""
echo "  UQC root:  $UQC_ROOT"
echo "  App dir:   $APP_DIR"
echo ""

# ── Step 1: Create directory structure ───────────────────────────────────────
echo "[1/5] Creating .app bundle structure..."
mkdir -p "$CONTENTS/MacOS"
mkdir -p "$CONTENTS/Resources"

# ── Step 2: Verify core files exist ──────────────────────────────────────────
echo "[2/5] Verifying core files..."
MISSING=0
for f in "$CONTENTS/MacOS/UQC" "$CONTENTS/Info.plist" "$CONTENTS/Resources/install_deps.sh"; do
    if [ ! -f "$f" ]; then
        echo "  ERROR: Missing $f"
        MISSING=1
    else
        echo "  OK: $f"
    fi
done
if [ "$MISSING" -eq 1 ]; then
    echo ""
    echo "ERROR: Missing core bundle files. Ensure you have:"
    echo "  - UQC.app/Contents/MacOS/UQC"
    echo "  - UQC.app/Contents/Info.plist"
    echo "  - UQC.app/Contents/Resources/install_deps.sh"
    exit 1
fi

# ── Step 3: Create symlink to UQC root ───────────────────────────────────────
echo "[3/5] Creating symlink to UQC root..."
SYMLINK="$CONTENTS/Resources/app"
if [ -L "$SYMLINK" ]; then
    rm "$SYMLINK"
fi
# Use relative symlink so the bundle is relocatable within the UQC directory
ln -s ../../../.. "$SYMLINK"
echo "  Symlink: Resources/app -> ../../../.. ($UQC_ROOT)"

# ── Step 4: Set permissions ──────────────────────────────────────────────────
echo "[4/5] Setting executable permissions..."
chmod +x "$CONTENTS/MacOS/UQC"
chmod +x "$CONTENTS/Resources/install_deps.sh"
echo "  Done."

# ── Step 5: Generate placeholder icon ────────────────────────────────────────
echo "[5/5] Checking icon..."
ICON="$CONTENTS/Resources/icon.icns"
if [ ! -f "$ICON" ]; then
    echo "  No icon.icns found — creating placeholder."
    # Create a minimal valid .icns (empty icon, macOS will use generic app icon)
    # The file just needs to exist; macOS falls back to default if it's invalid
    touch "$ICON"
    echo "  Placeholder created. Replace with a real .icns for a custom icon."
else
    echo "  Icon already exists."
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "──────────────────────────────────────────"
echo "  Build complete!"
echo ""
echo "  Bundle: $APP_DIR"
echo ""
echo "  To use:"
echo "    1. Copy the entire UQC/ folder to a Mac"
echo "    2. Double-click UQC/macos/UQC.app"
echo "    3. On first launch, dependencies install automatically"
echo "──────────────────────────────────────────"

# ── Optional: Create DMG ─────────────────────────────────────────────────────
if [[ "${1:-}" == "--dmg" ]]; then
    echo ""
    echo "Creating DMG..."
    DMG_NAME="UQC-macOS-Intel.dmg"
    DMG_PATH="$SCRIPT_DIR/$DMG_NAME"

    # Create a temporary directory with the full UQC tree
    STAGING="$(mktemp -d)"
    cp -a "$UQC_ROOT" "$STAGING/UQC"

    if command -v hdiutil &>/dev/null; then
        hdiutil create -volname "UQC" -srcfolder "$STAGING/UQC" \
            -ov -format UDZO "$DMG_PATH"
        echo "  DMG created: $DMG_PATH"
    else
        echo "  WARNING: hdiutil not available (not on macOS). Skipping DMG creation."
    fi

    rm -rf "$STAGING"
fi
