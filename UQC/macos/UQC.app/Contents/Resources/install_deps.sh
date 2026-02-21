#!/bin/bash
# ──────────────────────────────────────────────────────────────────────────────
# UQC — Universal Quantum Codec  |  macOS Dependency Installer
# Copyright 2026 Cyber Vines, LLC (cybervines.com)
# ──────────────────────────────────────────────────────────────────────────────
set -euo pipefail

echo "──────────────────────────────────────────"
echo "  UQC Dependency Installer for macOS"
echo "──────────────────────────────────────────"
echo ""

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
UQC_ROOT="$SCRIPT_DIR/app"
if [ -L "$UQC_ROOT" ]; then
    UQC_ROOT="$(cd "$UQC_ROOT" && pwd)"
fi
WEB_DIR="$UQC_ROOT/web"
BUILD_DIR="$HOME/.uqc_build"

# ── Step 1: Install Homebrew ─────────────────────────────────────────────────
echo "[1/7] Checking Homebrew..."
if ! command -v brew &>/dev/null; then
    echo "  Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add Homebrew to PATH for this session
    if [ -f /usr/local/bin/brew ]; then
        eval "$(/usr/local/bin/brew shellenv)"
    elif [ -f /opt/homebrew/bin/brew ]; then
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "  Homebrew already installed."
fi

# ── Step 2: Install system packages ─────────────────────────────────────────
echo ""
echo "[2/7] Installing system packages via Homebrew..."
BREW_PACKAGES=(hackrf python3 numpy espeak-ng sox cmake libusb)
for pkg in "${BREW_PACKAGES[@]}"; do
    if brew list "$pkg" &>/dev/null; then
        echo "  $pkg — already installed"
    else
        echo "  Installing $pkg..."
        brew install "$pkg"
    fi
done

# ── Step 3: Install Python packages ─────────────────────────────────────────
echo ""
echo "[3/7] Installing Python packages..."
REQUIREMENTS="$WEB_DIR/requirements.txt"
if [ -f "$REQUIREMENTS" ]; then
    pip3 install --user -r "$REQUIREMENTS"
else
    echo "  WARNING: requirements.txt not found at $REQUIREMENTS"
    echo "  Installing core packages manually..."
    pip3 install --user fastapi uvicorn websockets python-multipart numpy scipy
fi

# ── Step 4: Build whisper.cpp ────────────────────────────────────────────────
echo ""
echo "[4/7] Building whisper.cpp..."
mkdir -p "$BUILD_DIR"
WHISPER_DIR="$BUILD_DIR/whisper.cpp"
if [ -f /usr/local/bin/whisper-cli ] || [ -f /usr/local/bin/main-whisper ]; then
    echo "  whisper.cpp already installed."
else
    if [ ! -d "$WHISPER_DIR" ]; then
        git clone https://github.com/ggerganov/whisper.cpp.git "$WHISPER_DIR"
    fi
    cd "$WHISPER_DIR"
    git pull --ff-only 2>/dev/null || true
    cmake -B build -DCMAKE_BUILD_TYPE=Release
    cmake --build build --config Release -j "$(sysctl -n hw.ncpu)"
    # Install the binary
    if [ -f build/bin/whisper-cli ]; then
        sudo cp build/bin/whisper-cli /usr/local/bin/whisper-cli
    elif [ -f build/bin/main ]; then
        sudo cp build/bin/main /usr/local/bin/whisper-cli
    fi
    echo "  whisper.cpp built and installed."
fi

# ── Step 5: Build llama.cpp ──────────────────────────────────────────────────
echo ""
echo "[5/7] Building llama.cpp..."
LLAMA_DIR="$BUILD_DIR/llama.cpp"
if [ -f /usr/local/bin/llama-cli ] || [ -f /usr/local/bin/main-llama ]; then
    echo "  llama.cpp already installed."
else
    if [ ! -d "$LLAMA_DIR" ]; then
        git clone https://github.com/ggerganov/llama.cpp.git "$LLAMA_DIR"
    fi
    cd "$LLAMA_DIR"
    git pull --ff-only 2>/dev/null || true
    cmake -B build -DCMAKE_BUILD_TYPE=Release
    cmake --build build --config Release -j "$(sysctl -n hw.ncpu)"
    # Install the binary
    if [ -f build/bin/llama-cli ]; then
        sudo cp build/bin/llama-cli /usr/local/bin/llama-cli
    elif [ -f build/bin/main ]; then
        sudo cp build/bin/main /usr/local/bin/llama-cli
    fi
    echo "  llama.cpp built and installed."
fi

# ── Step 6: Download AI models ───────────────────────────────────────────────
echo ""
echo "[6/7] Downloading AI models..."
MODELS_DIR="$HOME/.uqc_models"
mkdir -p "$MODELS_DIR"

# Whisper base.en model
WHISPER_MODEL="$MODELS_DIR/ggml-base.en.bin"
if [ -f "$WHISPER_MODEL" ]; then
    echo "  Whisper model already downloaded."
else
    echo "  Downloading Whisper base.en model (~150 MB)..."
    curl -L -o "$WHISPER_MODEL" \
        "https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-base.en.bin"
fi

# Qwen 0.5B model (small enough for Intel Macs)
LLAMA_MODEL="$MODELS_DIR/qwen2.5-0.5b-instruct-q4_k_m.gguf"
if [ -f "$LLAMA_MODEL" ]; then
    echo "  LLM model already downloaded."
else
    echo "  Downloading Qwen 2.5 0.5B model (~400 MB)..."
    curl -L -o "$LLAMA_MODEL" \
        "https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct-GGUF/resolve/main/qwen2.5-0.5b-instruct-q4_k_m.gguf"
fi

# ── Step 7: Create directories ───────────────────────────────────────────────
echo ""
echo "[7/7] Creating directories..."
mkdir -p "$UQC_ROOT/hackrf_logs"

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo "──────────────────────────────────────────"
echo "  UQC dependency installation complete!"
echo ""
echo "  Whisper model: $WHISPER_MODEL"
echo "  LLM model:     $LLAMA_MODEL"
echo "  Build dir:     $BUILD_DIR"
echo "──────────────────────────────────────────"
