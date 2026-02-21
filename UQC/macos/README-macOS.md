# UQC for macOS (Intel)

**Universal Quantum Codec** — HackRF multi-mode RF TX/RX with web UI.

Copyright 2026 Cyber Vines, LLC ([cybervines.com](https://cybervines.com))

## Quick Start

1. Copy the entire `UQC/` folder to your Mac
2. Open `UQC/macos/UQC.app`
3. On first launch, UQC will install all dependencies automatically
4. The web UI opens in your default browser at `http://localhost:8080`

## First Launch

The first time you run UQC.app, it will:

1. Check for **Xcode Command Line Tools** (prompts to install if missing)
2. Install **Homebrew** (if not already installed)
3. Install system packages: `hackrf`, `python3`, `numpy`, `espeak-ng`, `sox`, `cmake`, `libusb`
4. Install Python packages from `web/requirements.txt`
5. Build **whisper.cpp** and **llama.cpp** from source (optimized for Intel)
6. Download AI models (~550 MB total):
   - Whisper base.en (~150 MB) for speech recognition
   - Qwen 2.5 0.5B (~400 MB) for AI voice responses

This process takes approximately 10-20 minutes depending on your internet connection.

## Requirements

- macOS 10.13 (High Sierra) or later
- Intel processor (x86_64)
- Internet connection (for first-launch setup)
- ~2 GB free disk space (dependencies + models)
- HackRF One (for RF operations)

## Building the .app Bundle

If you need to rebuild the bundle (e.g., after updating files):

```bash
cd UQC/macos
chmod +x build.sh
./build.sh
```

To also create a distributable DMG:

```bash
./build.sh --dmg
```

## Directory Structure

```
UQC/
├── transmit_modes.py          # Shared — core modulation engine
├── morse_transmit.sh          # Shared — CLI interface
├── web/server.py              # Shared — FastAPI backend
├── web/static/                # Shared — web frontend
├── hackrf_logs/               # Shared — log directory
└── macos/
    ├── build.sh               # Bundle builder script
    ├── README-macOS.md        # This file
    └── UQC.app/
        └── Contents/
            ├── Info.plist     # App manifest
            ├── MacOS/UQC      # Launcher script
            └── Resources/
                ├── icon.icns          # App icon
                ├── install_deps.sh    # Dependency installer
                └── app -> ../../../.. # Symlink to UQC root
```

## File Locations

After installation, dependencies are stored at:

| Item | Location |
|------|----------|
| Homebrew | `/usr/local` (Intel) |
| whisper.cpp binary | `/usr/local/bin/whisper-cli` |
| llama.cpp binary | `/usr/local/bin/llama-cli` |
| Whisper model | `~/.uqc_models/ggml-base.en.bin` |
| LLM model | `~/.uqc_models/qwen2.5-0.5b-instruct-q4_k_m.gguf` |
| Build sources | `~/.uqc_build/` |
| Install marker | `~/.uqc_installed` |

## Troubleshooting

### "UQC.app is damaged and can't be opened"

macOS Gatekeeper blocks unsigned apps. Remove the quarantine flag:

```bash
xattr -cr UQC/macos/UQC.app
```

### Server fails to start

1. Check that Python 3 is installed: `python3 --version`
2. Check that dependencies are installed: `pip3 list | grep fastapi`
3. Check if port 8080 is in use: `lsof -i :8080`
4. Try running the server manually:
   ```bash
   cd UQC/web
   python3 server.py
   ```

### HackRF not detected

1. Ensure HackRF is plugged in
2. Check with: `hackrf_info`
3. If not found, try: `brew reinstall hackrf libusb`

### Reinstalling dependencies

Delete the install marker and relaunch:

```bash
rm ~/.uqc_installed
```

Then double-click UQC.app again to trigger a fresh install.

### WebSocket connection issues

If the web UI connects but WebSocket features (live TX, AI voice) fail:

1. Verify `websockets` is installed: `pip3 show websockets`
2. If missing: `pip3 install --user websockets>=12.0`
3. Restart the app

### Cleaning up build artifacts

To remove build sources and models:

```bash
rm -rf ~/.uqc_build ~/.uqc_models ~/.uqc_installed
```
