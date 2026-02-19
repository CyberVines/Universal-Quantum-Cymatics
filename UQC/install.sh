#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# UQC — Universal Quantum Codec
# Environment Setup & Dependency Installer
# ═══════════════════════════════════════════════════════════════════════════════
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                                                                             │
# │  .------..------..------..------..------..------..------.         .------..------. │
# │  |W.--. ||E.--. ||L.--. ||C.--. ||O.--. ||M.--. ||E.--. | .-.     |T.--. ||O.--. | │
# │  | :/\: || (\/) || :/\: || :/\: || :/\: || (\/) || (\/) |((3))    | :/\: || :/\: | │
# │  | :\/: || :\/: || (__) || :\/: || :\/: || :\/: || :\/: | '-.-.   | (__) || :\/: | │
# │  | '--23|| '--'5|| '--12|| '--'3|| '--15|| '--13|| '--'5|  ((22)) | '--20|| '--15| │
# │  `------'`------'`------'`------'`------'`------'`------'    '-'  `------'`------' │
# │  .------..------..------..------..------.         .------..------..------..------..------. │
# │  |C.--. ||Y.--. ||B.--. ||E.--. ||R.--. | .-.     |V.--. ||I.--. ||N.--. ||E.--. ||S.--. | │
# │  | :/\: || (\/) || :(): || (\/) || :(): |((3))    | :(): || (\/) || :(): || (\/) || :/\: | │
# │  | :\/: || :\/: || ()() || :\/: || ()() | '-.-.   | ()() || :\/: || ()() || :\/: || :\/: | │
# │  | '--'3|| '--25|| '--'2|| '--'5|| '--18|  ((22)) | '--22|| '--'9|| '--14|| '--'5|| '--19| │
# │  `------'`------'`------'`------'`------'    '-'  `------'`------'`------'`------'`------' │
# │                                                                             │
# │  QR Code — https://cybervines.com                                           │
# │                                                                             │
# │  ██████████████  ██      ████        ██████████████                          │
# │  ██          ██  ██  ██  ██  ██  ██  ██          ██                          │
# │  ██  ██████  ██  ██  ████████████    ██  ██████  ██                          │
# │  ██  ██████  ██    ████    ████  ██  ██  ██████  ██                          │
# │  ██  ██████  ██  ██████████████  ██  ██  ██████  ██                          │
# │  ██          ██    ██      ████  ██  ██          ██                          │
# │  ██████████████  ██  ██  ██  ██  ██  ██████████████                          │
# │                          ██████████                                          │
# │  ██    ████████████      ██  ██  ████    ██  ██████                          │
# │    ████████    ██  ██  ██    ████  ██  ██████████                            │
# │  ██  ██      ████    ████████████████  ██  ██    ██                          │
# │          ████  ██    ██  ██  ██  ██  ██    ████████                          │
# │  ██    ██    ████      ██        ██  ████        ██                          │
# │  ████    ██      ██      ██  ██████      ██    ██                            │
# │  ████████    ████  ████      ██████  ██  ██████████                          │
# │  ██  ██████    ██████    ██    ██      ██  ████  ██                          │
# │  ██    ██  ████        ██████  ████████████  ████                            │
# │                  ████  ██  ██  ████      ██  ████                            │
# │  ██████████████  ██████  ████    ██  ██  ██      ██                          │
# │  ██          ██  ██    ██  ██  ████      ██                                  │
# │  ██  ██████  ██  ██    ██  ██  ████████████    ████                          │
# │  ██  ██████  ██  ██████  ██████    ████        ████                          │
# │  ██  ██████  ██        ██  ██  ██  ██    ██████████                          │
# │  ██          ██      ████████  ██    ██████  ██████                          │
# │  ██████████████  ██  ████████    ██  ██    ██    ██                          │
# │                                                                             │
# │  Copyright 12011 HE - 12026 HE Cyber Vines, LLC                            │
# │  All rights reserved.                                                       │
# │                                                                             │
# │  -----------------------------------------------------------------          │
# │  Warning: This system is restricted to private use                          │
# │  authorized users for business purposes only. Unauthorized access           │
# │  or use is a violation of company policy and the law. This system           │
# │  may be monitored for administrative and security reasons. By               │
# │  proceeding, you acknowledge that (1) you have read and understand          │
# │  this notice and (2) you consent to the system monitoring.                  │
# │                                                                             │
# │  This Website is intended only for use by 'Authorized Personnel'            │
# │  and may contain legally privileged and/or confidential information.        │
# │  This Website, including any files and attachments, is covered by           │
# │  the Electronic Communications Privacy Act, 18 U.S.C. 2510-2522            │
# │  and should not be disclosed to third parties. If you are not the           │
# │  intended recipient, you are hereby notified that any dissemination,        │
# │  distribution, use for any reason, or copying is strictly prohibited.       │
# │  For support, please immediately notify Cyber Vines, LLC                    │
# │  at webadmin@cybervines.com or phone +1 214 295 8481                        │
# │                                                                             │
# │  Although Cyber Vines, LLC has attempted to ensure the accuracy of          │
# │  the technical support information it is possible that it may contain       │
# │  technical inaccuracies, typographical, or other errors.                    │
# │  Cyber Vines, LLC assumes no liability for any errors in this               │
# │  information, and for damages, whether direct, indirect, incidental,        │
# │  and consequential or otherwise, that may result from such error,           │
# │  including, but not limited to loss of data or profits.                     │
# │                                                                             │
# │  Our website follows the safe harbor provisions of 17 U.S.C. §512,         │
# │  otherwise known as Digital Millennium Copyright Act ("DMCA").              │
# │  To file a copyright infringement notification with us, you will            │
# │  need to send a written communication that includes substantially           │
# │  the following:                                                             │
# │                                                                             │
# │  A physical or electronic signature of a person authorized to act           │
# │  on behalf of the owner of an exclusive right that is allegedly             │
# │  infringed.                                                                 │
# │                                                                             │
# │  Identification of the copyrighted work claimed to have been                │
# │  infringed, or, if multiple copyrighted works at a single online            │
# │  site are covered by a single notification, a representative list           │
# │  of such works at that site.                                                │
# │                                                                             │
# │  Identification of the material that is claimed to be infringing            │
# │  or to be the subject of infringing activity and that is to be              │
# │  removed or access to which is to be disabled, and information              │
# │  reasonably sufficient to permit the service provider to locate             │
# │  the material. Providing URLs in the body of an email is the best           │
# │  way to help us locate content quickly.                                     │
# │                                                                             │
# │  Information reasonably sufficient to permit the service provider           │
# │  to contact the complaining party, such as an address, telephone            │
# │  number, and, if available, an electronic mail address at which             │
# │  the complaining party may be contacted.                                    │
# │                                                                             │
# │  A statement that the complaining party has a good faith belief             │
# │  that use of the material in the manner complained of is not                │
# │  authorized by the copyright owner, its agent, or the law.                  │
# │                                                                             │
# │  A statement that the information in the notification is accurate,          │
# │  and under penalty of perjury, that the complaining party is                │
# │  authorized to act on behalf of the owner of an exclusive right             │
# │  that is allegedly infringed (Note that under Section 512(f) any            │
# │  person who knowingly and materially misrepresents that material            │
# │  or activity is infringing may be subject to liability for damages.         │
# │                                                                             │
# │  All basic services start at $89 per hour...                                │
# │  -----------------------------------------------------------------          │
# │                                                                             │
# └─────────────────────────────────────────────────────────────────────────────┘
#
#
# Supports: Debian/Ubuntu, Fedora/RHEL/CentOS, Arch/Manjaro, openSUSE, Alpine,
#           Void, Gentoo, NixOS, and generic Linux with manual guidance.
#
# Installs:
#   - System packages (hackrf, python3, numpy, espeak-ng, build tools, bc, etc.)
#   - whisper.cpp (speech-to-text for option 5)
#   - llama.cpp  (local LLM for option 5)
#   - Whisper base.en model
#   - Qwen2.5-1.5B LLM model
#
# Usage:
#   chmod +x install.sh
#   ./install.sh
#
# ═══════════════════════════════════════════════════════════════════════════════

set -euo pipefail

UQC_DIR="$(cd "$(dirname "$0")" && pwd)"
WHISPER_DIR="$UQC_DIR/whisper.cpp"
LLAMA_DIR="$UQC_DIR/llama.cpp"
LLAMA_MODEL_DIR="$LLAMA_DIR/models"
WHISPER_MODEL_DIR="$WHISPER_DIR/models"
LLAMA_MODEL_URL="https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"
WHISPER_MODEL="base.en"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

log()   { echo -e "${GREEN}[+]${NC} $*"; }
warn()  { echo -e "${YELLOW}[!]${NC} $*"; }
err()   { echo -e "${RED}[x]${NC} $*"; }
info()  { echo -e "${CYAN}[i]${NC} $*"; }
header(){ echo -e "\n${BOLD}═══ $* ═══${NC}\n"; }

# ── Detect distro ─────────────────────────────────────────────────────────────
detect_distro() {
    if [[ -f /etc/os-release ]]; then
        . /etc/os-release
        DISTRO_ID="${ID:-unknown}"
        DISTRO_LIKE="${ID_LIKE:-}"
        DISTRO_NAME="${PRETTY_NAME:-$DISTRO_ID}"
    elif [[ -f /etc/debian_version ]]; then
        DISTRO_ID="debian"
        DISTRO_LIKE="debian"
        DISTRO_NAME="Debian $(cat /etc/debian_version)"
    elif [[ -f /etc/redhat-release ]]; then
        DISTRO_ID="rhel"
        DISTRO_LIKE="rhel fedora"
        DISTRO_NAME="$(cat /etc/redhat-release)"
    else
        DISTRO_ID="unknown"
        DISTRO_LIKE=""
        DISTRO_NAME="Unknown Linux"
    fi

    # Classify into package manager family
    if echo "$DISTRO_ID $DISTRO_LIKE" | grep -qiE 'debian|ubuntu|mint|pop|kali|raspbian|elementary|zorin|mx|lmde|parrot'; then
        PKG_FAMILY="apt"
    elif echo "$DISTRO_ID $DISTRO_LIKE" | grep -qiE 'fedora|rhel|centos|rocky|alma|oracle|amzn|nobara'; then
        PKG_FAMILY="dnf"
    elif echo "$DISTRO_ID $DISTRO_LIKE" | grep -qiE 'arch|manjaro|endeavour|garuda|artix'; then
        PKG_FAMILY="pacman"
    elif echo "$DISTRO_ID $DISTRO_LIKE" | grep -qiE 'suse|opensuse'; then
        PKG_FAMILY="zypper"
    elif echo "$DISTRO_ID" | grep -qiE 'alpine'; then
        PKG_FAMILY="apk"
    elif echo "$DISTRO_ID" | grep -qiE 'void'; then
        PKG_FAMILY="xbps"
    elif echo "$DISTRO_ID" | grep -qiE 'gentoo'; then
        PKG_FAMILY="emerge"
    elif echo "$DISTRO_ID" | grep -qiE 'nixos|nix'; then
        PKG_FAMILY="nix"
    else
        PKG_FAMILY="unknown"
    fi
}

# ── Privilege escalation ──────────────────────────────────────────────────────
SUDO=""
setup_sudo() {
    if [[ $EUID -ne 0 ]]; then
        if command -v sudo &>/dev/null; then
            SUDO="sudo"
            info "Will use sudo for package installation."
        elif command -v doas &>/dev/null; then
            SUDO="doas"
            info "Will use doas for package installation."
        else
            warn "Not running as root and no sudo/doas found."
            warn "Package installation may fail — run as root if needed."
        fi
    fi
}

# ── Package installation per distro ───────────────────────────────────────────
install_system_packages() {
    header "Installing System Packages"

    case "$PKG_FAMILY" in
        apt)
            log "Updating apt package lists..."
            $SUDO apt-get update -qq

            log "Installing packages via apt..."
            $SUDO apt-get install -y \
                build-essential \
                git \
                cmake \
                python3 \
                python3-pip \
                python3-numpy \
                python3-venv \
                hackrf \
                libhackrf-dev \
                espeak-ng \
                bc \
                wget \
                curl \
                libsdl2-dev \
                pkg-config \
                sox \
                2>&1 | tail -3
            ;;

        dnf)
            log "Installing packages via dnf..."
            # Determine if we need dnf or yum
            PKG_CMD="dnf"
            if ! command -v dnf &>/dev/null; then
                PKG_CMD="yum"
            fi
            $SUDO $PKG_CMD install -y \
                gcc gcc-c++ make \
                git \
                cmake \
                python3 \
                python3-pip \
                python3-numpy \
                hackrf \
                hackrf-devel \
                espeak-ng \
                bc \
                wget \
                curl \
                SDL2-devel \
                pkg-config \
                sox \
                2>&1 | tail -3

            # EPEL may be needed on RHEL/CentOS/Rocky
            if echo "$DISTRO_ID $DISTRO_LIKE" | grep -qiE 'rhel|centos|rocky|alma'; then
                if ! rpm -q epel-release &>/dev/null; then
                    warn "EPEL not found — some packages may be missing."
                    warn "Install with: sudo dnf install epel-release"
                fi
            fi
            ;;

        pacman)
            log "Installing packages via pacman..."
            $SUDO pacman -Syu --noconfirm --needed \
                base-devel \
                git \
                cmake \
                python \
                python-pip \
                python-numpy \
                hackrf \
                espeak-ng \
                bc \
                wget \
                curl \
                sdl2 \
                pkg-config \
                sox \
                2>&1 | tail -3
            ;;

        zypper)
            log "Installing packages via zypper..."
            $SUDO zypper install -y \
                -t pattern devel_basis \
                git \
                cmake \
                python3 \
                python3-pip \
                python3-numpy \
                hackrf \
                libhackrf-devel \
                espeak-ng \
                bc \
                wget \
                curl \
                libSDL2-devel \
                pkg-config \
                sox \
                2>&1 | tail -3
            ;;

        apk)
            log "Installing packages via apk..."
            $SUDO apk add --no-cache \
                build-base \
                git \
                cmake \
                python3 \
                py3-pip \
                py3-numpy \
                hackrf \
                hackrf-dev \
                espeak-ng \
                bc \
                wget \
                curl \
                sdl2-dev \
                pkgconf \
                sox \
                2>&1 | tail -3
            ;;

        xbps)
            log "Installing packages via xbps..."
            $SUDO xbps-install -Sy \
                base-devel \
                git \
                cmake \
                python3 \
                python3-pip \
                python3-numpy \
                hackrf \
                hackrf-devel \
                espeak-ng \
                bc \
                wget \
                curl \
                SDL2-devel \
                pkg-config \
                sox \
                2>&1 | tail -3
            ;;

        emerge)
            log "Installing packages via emerge..."
            $SUDO emerge --ask=n \
                dev-vcs/git \
                dev-build/cmake \
                dev-lang/python \
                dev-python/numpy \
                net-wireless/hackrf-tools \
                app-accessibility/espeak-ng \
                sys-devel/bc \
                net-misc/wget \
                net-misc/curl \
                media-libs/libsdl2 \
                media-sound/sox \
                2>&1 | tail -3
            ;;

        nix)
            log "NixOS detected — add these to your configuration.nix or use nix-shell:"
            info "  nix-shell -p gcc git cmake python3 python3Packages.numpy hackrf espeak-ng bc wget curl SDL2 sox"
            warn "Proceeding with nix-env for user packages..."
            nix-env -iA nixpkgs.gcc nixpkgs.git nixpkgs.cmake \
                nixpkgs.python3 nixpkgs.python3Packages.numpy \
                nixpkgs.hackrf nixpkgs.espeak-ng nixpkgs.bc \
                nixpkgs.wget nixpkgs.curl nixpkgs.SDL2 nixpkgs.sox \
                2>&1 | tail -3 || true
            ;;

        *)
            warn "Unrecognized package manager for: $DISTRO_NAME"
            warn "Please manually install these packages:"
            echo "  - gcc/g++, make, cmake, git"
            echo "  - python3, python3-pip, python3-numpy"
            echo "  - hackrf (hackrf_transfer)"
            echo "  - espeak-ng"
            echo "  - bc, wget, curl, sox"
            echo "  - SDL2 development libraries"
            echo ""
            read -rp "Press Enter to continue anyway, or Ctrl+C to abort... " _
            ;;
    esac

    log "System packages done."
}

# ── Python numpy fallback ─────────────────────────────────────────────────────
ensure_numpy() {
    header "Checking Python / NumPy"

    if ! command -v python3 &>/dev/null; then
        err "python3 not found! Cannot continue."
        exit 1
    fi

    PYTHON_VER=$(python3 --version 2>&1)
    log "Python: $PYTHON_VER"

    if python3 -c "import numpy" 2>/dev/null; then
        NP_VER=$(python3 -c "import numpy; print(numpy.__version__)")
        log "NumPy $NP_VER already installed."
    else
        warn "NumPy not found via system package. Installing via pip..."
        if python3 -m pip --version &>/dev/null; then
            python3 -m pip install --user --break-system-packages numpy 2>/dev/null \
                || python3 -m pip install --user numpy 2>/dev/null \
                || $SUDO python3 -m pip install numpy 2>/dev/null \
                || { err "Failed to install numpy. Please install manually: pip3 install numpy"; exit 1; }
            log "NumPy installed via pip."
        else
            err "pip not available. Install python3-pip and try again."
            exit 1
        fi
    fi
}

# ── hackrf_transfer check ─────────────────────────────────────────────────────
check_hackrf() {
    header "Checking HackRF Tools"

    if command -v hackrf_transfer &>/dev/null; then
        log "hackrf_transfer found: $(which hackrf_transfer)"
        # Try hackrf_info if device present (non-fatal)
        hackrf_info 2>/dev/null | head -5 || info "No HackRF device connected (OK for now)."
    else
        warn "hackrf_transfer not found in PATH."
        warn "If you installed hackrf but it's not in PATH, add it:"
        warn "  export PATH=\$PATH:/usr/local/bin"
        warn "Or install hackrf tools for your distro."

        # Try building from source as fallback
        read -rp "Attempt to build hackrf from source? [y/N]: " BUILD_HRF
        if [[ "$BUILD_HRF" =~ ^[Yy] ]]; then
            build_hackrf_from_source
        fi
    fi
}

build_hackrf_from_source() {
    log "Building hackrf from source..."
    HACKRF_BUILD_DIR=$(mktemp -d)
    git clone --depth 1 https://github.com/greatscottgadgets/hackrf.git "$HACKRF_BUILD_DIR/hackrf"
    cd "$HACKRF_BUILD_DIR/hackrf/host"
    mkdir -p build && cd build
    cmake .. -DCMAKE_INSTALL_PREFIX=/usr/local
    make -j"$(nproc)"
    $SUDO make install
    $SUDO ldconfig 2>/dev/null || true
    cd "$UQC_DIR"
    rm -rf "$HACKRF_BUILD_DIR"
    log "hackrf tools installed from source."
}

# ── whisper.cpp ───────────────────────────────────────────────────────────────
setup_whisper() {
    header "Setting Up whisper.cpp (Speech-to-Text)"

    if [[ -x "$WHISPER_DIR/main" ]]; then
        log "whisper.cpp already built at $WHISPER_DIR/main"
    else
        if [[ -d "$WHISPER_DIR/.git" ]]; then
            log "whisper.cpp repo exists, rebuilding..."
        else
            log "Cloning whisper.cpp v1.5.5..."
            rm -rf "$WHISPER_DIR"
            git clone --depth 1 --branch v1.5.5 \
                https://github.com/ggerganov/whisper.cpp.git "$WHISPER_DIR"
        fi

        log "Building whisper.cpp..."
        cd "$WHISPER_DIR"
        make clean 2>/dev/null || true
        make -j"$(nproc)" main
        cd "$UQC_DIR"

        if [[ -x "$WHISPER_DIR/main" ]]; then
            log "whisper.cpp built successfully."
        else
            err "whisper.cpp build failed!"
            warn "Option 5 (AI voice responder) will not work."
            warn "Try building manually:"
            warn "  cd $WHISPER_DIR && make -j\$(nproc) main"
        fi
    fi

    # Download model
    WHISPER_MODEL_FILE="$WHISPER_MODEL_DIR/ggml-${WHISPER_MODEL}.bin"
    if [[ -f "$WHISPER_MODEL_FILE" ]]; then
        log "Whisper model '${WHISPER_MODEL}' already downloaded."
    else
        log "Downloading Whisper model '${WHISPER_MODEL}'..."
        if [[ -x "$WHISPER_MODEL_DIR/download-ggml-model.sh" ]]; then
            bash "$WHISPER_MODEL_DIR/download-ggml-model.sh" "$WHISPER_MODEL"
        else
            # Direct download fallback
            WHISPER_DL_URL="https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-${WHISPER_MODEL}.bin"
            mkdir -p "$WHISPER_MODEL_DIR"
            wget -q --show-progress -O "$WHISPER_MODEL_FILE" "$WHISPER_DL_URL" \
                || curl -L -o "$WHISPER_MODEL_FILE" "$WHISPER_DL_URL" \
                || { err "Failed to download Whisper model."; }
        fi

        if [[ -f "$WHISPER_MODEL_FILE" ]]; then
            log "Whisper model downloaded: $(du -h "$WHISPER_MODEL_FILE" | cut -f1)"
        fi
    fi
}

# ── llama.cpp ─────────────────────────────────────────────────────────────────
setup_llama() {
    header "Setting Up llama.cpp (Local LLM)"

    LLAMA_BIN="$LLAMA_DIR/llama-cli"
    # Also check for older binary name
    [[ ! -x "$LLAMA_BIN" ]] && LLAMA_BIN="$LLAMA_DIR/main"

    if [[ -x "$LLAMA_BIN" ]]; then
        log "llama.cpp already built at $LLAMA_BIN"
    else
        if [[ -d "$LLAMA_DIR/.git" ]]; then
            log "llama.cpp repo exists, rebuilding..."
        else
            log "Cloning llama.cpp (b4000)..."
            rm -rf "$LLAMA_DIR"
            git clone --depth 1 --branch b4000 \
                https://github.com/ggerganov/llama.cpp.git "$LLAMA_DIR"
        fi

        log "Building llama.cpp..."
        cd "$LLAMA_DIR"
        make clean 2>/dev/null || true
        make -j"$(nproc)" llama-cli 2>/dev/null || make -j"$(nproc)" main 2>/dev/null || true
        cd "$UQC_DIR"

        # Check which binary was built
        if [[ -x "$LLAMA_DIR/llama-cli" ]]; then
            log "llama.cpp built successfully (llama-cli)."
        elif [[ -x "$LLAMA_DIR/main" ]]; then
            log "llama.cpp built successfully (main)."
        else
            err "llama.cpp build failed!"
            warn "Option 5 (AI voice responder) will not work."
            warn "Try building manually:"
            warn "  cd $LLAMA_DIR && make -j\$(nproc) llama-cli"
        fi
    fi

    # Download LLM model
    LLAMA_MODEL_FILE="$LLAMA_MODEL_DIR/qwen2.5-1.5b-instruct-q4_k_m.gguf"
    if [[ -f "$LLAMA_MODEL_FILE" ]]; then
        log "LLM model already downloaded: $(du -h "$LLAMA_MODEL_FILE" | cut -f1)"
    else
        log "Downloading Qwen2.5-1.5B LLM model (~1 GB)..."
        mkdir -p "$LLAMA_MODEL_DIR"
        wget -q --show-progress -O "$LLAMA_MODEL_FILE" "$LLAMA_MODEL_URL" \
            || curl -L -o "$LLAMA_MODEL_FILE" "$LLAMA_MODEL_URL" \
            || { err "Failed to download LLM model."; warn "Download manually:"; warn "  wget -O $LLAMA_MODEL_FILE $LLAMA_MODEL_URL"; }

        if [[ -f "$LLAMA_MODEL_FILE" ]]; then
            log "LLM model downloaded: $(du -h "$LLAMA_MODEL_FILE" | cut -f1)"
        fi
    fi
}

# ── Set permissions ───────────────────────────────────────────────────────────
set_permissions() {
    header "Setting Permissions"

    chmod +x "$UQC_DIR/morse_transmit.sh"
    chmod +x "$UQC_DIR/transmit_modes.py"
    chmod +x "$UQC_DIR/install.sh"
    log "Scripts marked executable."

    # udev rules for HackRF (so it works without root)
    UDEV_RULE="/etc/udev/rules.d/52-hackrf.rules"
    if [[ ! -f "$UDEV_RULE" ]]; then
        log "Installing udev rules for HackRF (non-root USB access)..."
        echo 'ATTR{idVendor}=="1d50", ATTR{idProduct}=="604b", SYMLINK+="hackrf-jawbreaker-%k", MODE="660", GROUP="plugdev"
ATTR{idVendor}=="1d50", ATTR{idProduct}=="6089", SYMLINK+="hackrf-one-%k", MODE="660", GROUP="plugdev"
ATTR{idVendor}=="1d50", ATTR{idProduct}=="cc15", SYMLINK+="rad1o-%k", MODE="660", GROUP="plugdev"' \
            | $SUDO tee "$UDEV_RULE" > /dev/null 2>/dev/null && {
            $SUDO udevadm control --reload-rules 2>/dev/null || true
            $SUDO udevadm trigger 2>/dev/null || true
            log "udev rules installed."
        } || warn "Could not install udev rules (non-fatal)."

        # Add user to plugdev group
        if getent group plugdev &>/dev/null; then
            if ! id -nG "$USER" | grep -qw plugdev; then
                $SUDO usermod -aG plugdev "$USER" 2>/dev/null \
                    && log "Added $USER to plugdev group (log out/in to take effect)." \
                    || warn "Could not add $USER to plugdev group."
            fi
        fi
    else
        log "udev rules already present."
    fi
}

# ── Update morse_transmit.sh paths ───────────────────────────────────────────
update_paths() {
    header "Updating Script Paths"

    # The script uses SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)" which is already
    # self-referencing. whisper.cpp and llama.cpp paths use $SCRIPT_DIR so they
    # should resolve to UQC/whisper.cpp and UQC/llama.cpp automatically.
    log "Scripts use self-referencing SCRIPT_DIR — paths are portable."

    # Verify the paths will resolve
    if [[ -d "$WHISPER_DIR" ]]; then
        log "whisper.cpp: $WHISPER_DIR"
    fi
    if [[ -d "$LLAMA_DIR" ]]; then
        log "llama.cpp: $LLAMA_DIR"
    fi
}

# ── Verification ──────────────────────────────────────────────────────────────
verify_installation() {
    header "Verification"

    PASS=0
    FAIL=0
    WARN_COUNT=0

    check_item() {
        local name="$1"
        local cmd="$2"
        if eval "$cmd" &>/dev/null; then
            log "$name — OK"
            PASS=$((PASS + 1))
        else
            err "$name — MISSING"
            FAIL=$((FAIL + 1))
        fi
    }

    check_warn() {
        local name="$1"
        local cmd="$2"
        if eval "$cmd" &>/dev/null; then
            log "$name — OK"
            PASS=$((PASS + 1))
        else
            warn "$name — not available (optional)"
            WARN_COUNT=$((WARN_COUNT + 1))
        fi
    }

    echo ""
    info "Core dependencies:"
    check_item "python3"           "command -v python3"
    check_item "numpy"             "python3 -c 'import numpy'"
    check_item "bash"              "command -v bash"
    check_item "bc"                "command -v bc"
    check_item "git"               "command -v git"
    check_item "make"              "command -v make"
    check_item "morse_transmit.sh" "test -x '$UQC_DIR/morse_transmit.sh'"
    check_item "transmit_modes.py" "test -x '$UQC_DIR/transmit_modes.py'"
    check_item "Python syntax"     "python3 -c \"import py_compile; py_compile.compile('$UQC_DIR/transmit_modes.py', doraise=True)\""
    check_item "Bash syntax"       "bash -n '$UQC_DIR/morse_transmit.sh'"

    echo ""
    info "RF hardware:"
    check_warn "hackrf_transfer"   "command -v hackrf_transfer"

    echo ""
    info "Audio/speech (for options 4-5):"
    check_warn "espeak-ng"         "command -v espeak-ng"

    echo ""
    info "AI voice responder (option 5):"
    check_warn "whisper.cpp"       "test -x '$WHISPER_DIR/main'"
    check_warn "Whisper model"     "test -f '$WHISPER_MODEL_DIR/ggml-${WHISPER_MODEL}.bin'"
    check_warn "llama.cpp"         "test -x '$LLAMA_DIR/llama-cli' -o -x '$LLAMA_DIR/main'"
    check_warn "LLM model"        "test -f '$LLAMA_MODEL_DIR/qwen2.5-1.5b-instruct-q4_k_m.gguf'"

    echo ""
    echo "─────────────────────────────────────────"
    echo -e "  ${GREEN}Passed: $PASS${NC}  ${RED}Failed: $FAIL${NC}  ${YELLOW}Warnings: $WARN_COUNT${NC}"
    echo "─────────────────────────────────────────"

    if [[ $FAIL -gt 0 ]]; then
        err "$FAIL required dependencies missing."
        warn "Core features (options 1-4, 6-8) require: python3, numpy, hackrf, bc"
        warn "Option 5 (AI voice) additionally requires: whisper.cpp, llama.cpp, espeak-ng"
        return 1
    else
        log "All required dependencies satisfied."
        if [[ $WARN_COUNT -gt 0 ]]; then
            info "Some optional components missing — related features will be unavailable."
        fi
        return 0
    fi
}

# ── Print final summary ──────────────────────────────────────────────────────
print_summary() {
    echo ""
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}  UQC Installation Complete${NC}"
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "  Location: $UQC_DIR"
    echo ""
    echo "  To run:"
    echo "    cd $UQC_DIR"
    echo "    ./morse_transmit.sh"
    echo ""
    echo "  Options available:"
    echo "    1) Compose & transmit message (30+ modulation modes)"
    echo "    2) Transmit raw IQ capture file"
    echo "    3) Record from HackRF and retransmit"
    echo "    4) Text-to-speech transmit"
    echo "    5) AI voice responder (listen → AI → speak)"
    echo "    6) Signal analyzer/decoder (listen → identify → decode)"
    echo "    7) Jitter frequency data (peaks/valleys → cipher/gematria/math)"
    echo "    8) Anomaly repository (view/search/export all logged events)"
    echo ""
    echo "  Log repository: $UQC_DIR/hackrf_logs/"
    echo ""
    echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
}

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

echo ""
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}  UQC — Universal Quantum Codec${NC}"
echo -e "${BOLD}  Environment Setup & Dependency Installer${NC}"
echo -e "${BOLD}═══════════════════════════════════════════════════════════════${NC}"
echo ""

detect_distro
log "Detected: $DISTRO_NAME (family: $PKG_FAMILY)"
echo ""

# Check if user wants full install or just verify
echo "Installation options:"
echo "  1) Full install (system packages + whisper.cpp + llama.cpp + models)"
echo "  2) Core only (system packages — no AI voice responder components)"
echo "  3) Verify only (check what's already installed)"
echo ""
read -rp "Enter choice [1-3]: " INSTALL_CHOICE

setup_sudo

case "$INSTALL_CHOICE" in
    1)
        install_system_packages
        ensure_numpy
        check_hackrf
        setup_whisper
        setup_llama
        set_permissions
        update_paths
        verify_installation || true
        print_summary
        ;;
    2)
        install_system_packages
        ensure_numpy
        check_hackrf
        set_permissions
        update_paths
        verify_installation || true
        print_summary
        ;;
    3)
        ensure_numpy 2>/dev/null || true
        verify_installation || true
        ;;
    *)
        err "Invalid choice."
        exit 1
        ;;
esac
