#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════════════
# HackRF Multi-Mode Transmitter
# Supports: CW, PSK, FSK/RTTY, MFSK, Olivia, FT8/FT4/WSPR/JT65,
#           AM, FM, SSB, AX.25, APRS
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

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SAMPLE_RATE=8000000
TX_GAIN=47
WPM=43
TONE_FREQ=572
F_DEV=5000
CALLSIGN="N0CALL"

echo "========================================="
echo "    HackRF Multi-Mode Transmitter"
echo "========================================="
echo ""

# ── Step 1: Frequency ──────────────────────────────────────────────────────
read -rp "Enter transmit frequency in MHz (e.g. 462.700): " FREQ_MHZ
[[ -z "$FREQ_MHZ" ]] && { echo "Error: No frequency entered."; exit 1; }
FREQUENCY=$(echo "$FREQ_MHZ * 1000000 / 1" | bc)

# ── Step 2: Source ────────────────────────────────────────────────────────
echo ""
echo "Transmit source:"
echo "  1) Compose a message"
echo "  2) Transmit a .raw IQ capture file"
echo "  3) Record from audio input and transmit"
echo "  4) Text-to-speech transmit"
echo "  5) AI voice responder (listen → AI → speak)"
echo "  6) Signal analyzer/decoder (listen → identify → decode)"
echo "  7) Jitter frequency data (peaks/valleys → binary → cipher/gematria analysis)"
echo "  8) Anomaly repository (view/search/export all logged events & anomalies)"
read -rp "Enter choice [1-8]: " TX_SOURCE

if [[ "$TX_SOURCE" == "2" ]]; then
    read -rp "Enter path to .raw file: " RAW_FILE
    RAW_FILE="${RAW_FILE/#\~/$HOME}"
    [[ ! -f "$RAW_FILE" ]] && { echo "Error: File not found: $RAW_FILE"; exit 1; }

    FILE_SIZE=$(stat -c%s "$RAW_FILE" 2>/dev/null || stat -f%z "$RAW_FILE" 2>/dev/null)
    DURATION=$(echo "scale=2; $FILE_SIZE / ($SAMPLE_RATE * 2)" | bc)
    echo "  File size: $(numfmt --to=iec "$FILE_SIZE" 2>/dev/null || echo "${FILE_SIZE} bytes")"
    echo "  Duration:  ~${DURATION}s at $(echo "scale=1; $SAMPLE_RATE / 1000000" | bc) MHz sample rate"

    echo ""
    echo "How many times to transmit?"
    echo "  Enter a number (e.g. 5), or 0 for continuous loop."
    echo "  Press Enter for a single transmission."
    read -rp "Repeat count [1]: " REPEAT_COUNT
    REPEAT_COUNT="${REPEAT_COUNT:-1}"
    if ! [[ "$REPEAT_COUNT" =~ ^[0-9]+$ ]]; then
        echo "Error: Invalid number."; exit 1
    fi

    if [[ "$REPEAT_COUNT" -eq 0 ]]; then
        REPEAT_LABEL="continuous (Ctrl+C to stop)"
    else
        REPEAT_LABEL="${REPEAT_COUNT}"
    fi
    echo ""
    echo "========================================="
    echo " Frequency : ${FREQ_MHZ} MHz"
    echo " Source    : ${RAW_FILE}"
    echo " TX Gain   : ${TX_GAIN} dB + RF amp"
    echo " Repeat    : ${REPEAT_LABEL}"
    echo "========================================="

    RAW_TX_CMD() {
        hackrf_transfer -t "$RAW_FILE" -f "$FREQUENCY" -s "$SAMPLE_RATE" -x "$TX_GAIN" -a 1 2>&1
    }

    if [[ "$REPEAT_COUNT" -eq 0 ]]; then
        echo "Transmitting (continuous loop — Ctrl+C to stop)..."
        COUNT=1
        trap 'echo ""; echo "Stopped after ${COUNT} transmission(s)."; exit 0' INT
        while true; do
            echo "── Transmission #${COUNT} ──"
            RAW_TX_CMD
            COUNT=$((COUNT + 1))
            sleep 0.5
        done
    elif [[ "$REPEAT_COUNT" -eq 1 ]]; then
        echo "Transmitting..."
        RAW_TX_CMD
        echo "Transmission complete."
    else
        echo "Transmitting ${REPEAT_COUNT} times..."
        for ((i=1; i<=REPEAT_COUNT; i++)); do
            echo "── Transmission ${i}/${REPEAT_COUNT} ──"
            RAW_TX_CMD
            [[ "$i" -lt "$REPEAT_COUNT" ]] && sleep 0.5
        done
        echo "All ${REPEAT_COUNT} transmissions complete."
    fi
    exit 0
fi

if [[ "$TX_SOURCE" == "3" ]]; then
    # ── Record IQ from HackRF and retransmit ─────────────────────────────
    echo ""
    read -rp "Receive frequency in MHz [${FREQ_MHZ}]: " RX_FREQ_MHZ
    RX_FREQ_MHZ="${RX_FREQ_MHZ:-$FREQ_MHZ}"
    RX_FREQUENCY=$(echo "$RX_FREQ_MHZ * 1000000 / 1" | bc)

    echo ""
    echo "RF receive gain:"
    read -rp "  LNA gain (0-40 dB, step 8) [16]: " LNA_GAIN
    LNA_GAIN="${LNA_GAIN:-16}"
    read -rp "  VGA gain (0-62 dB, step 2) [20]: " VGA_GAIN
    VGA_GAIN="${VGA_GAIN:-20}"

    REC_FILE=$(mktemp /tmp/hackrf_capture_XXXXXX.raw)

    echo ""
    echo "Recording on ${RX_FREQ_MHZ} MHz..."
    echo "Press Ctrl+C to stop recording."
    echo ""

    # Run in background for clean signal handling
    hackrf_transfer -r "$REC_FILE" -f "$RX_FREQUENCY" -s "$SAMPLE_RATE" \
        -l "$LNA_GAIN" -g "$VGA_GAIN" &
    HRF_PID=$!

    # Ctrl+C sends SIGINT to hackrf_transfer, then we wait for it to flush
    trap 'kill -INT $HRF_PID 2>/dev/null' INT
    wait $HRF_PID 2>/dev/null
    trap - INT
    sync

    if [[ ! -s "$REC_FILE" ]]; then
        echo "Error: No data recorded."
        rm -f "$REC_FILE"; exit 1
    fi

    FILE_SIZE=$(stat -c%s "$REC_FILE" 2>/dev/null || stat -f%z "$REC_FILE" 2>/dev/null)
    DURATION=$(echo "scale=2; $FILE_SIZE / ($SAMPLE_RATE * 2)" | bc)
    echo ""
    echo "Captured $(numfmt --to=iec "$FILE_SIZE" 2>/dev/null || echo "${FILE_SIZE} bytes") (~${DURATION}s)"

    echo ""
    echo "How many times to transmit?"
    echo "  Enter a number (e.g. 5), or 0 for continuous loop."
    echo "  Press Enter for a single transmission."
    read -rp "Repeat count [1]: " REPEAT_COUNT
    REPEAT_COUNT="${REPEAT_COUNT:-1}"
    if ! [[ "$REPEAT_COUNT" =~ ^[0-9]+$ ]]; then
        echo "Error: Invalid number."; rm -f "$REC_FILE"; exit 1
    fi

    if [[ "$REPEAT_COUNT" -eq 0 ]]; then
        REPEAT_LABEL="continuous (Ctrl+C to stop)"
    else
        REPEAT_LABEL="${REPEAT_COUNT}"
    fi
    echo ""
    echo "========================================="
    echo " RX Freq   : ${RX_FREQ_MHZ} MHz"
    echo " TX Freq   : ${FREQ_MHZ} MHz"
    echo " Capture   : ~${DURATION}s"
    echo " TX Gain   : ${TX_GAIN} dB + RF amp"
    echo " Repeat    : ${REPEAT_LABEL}"
    echo "========================================="

    REC_TX_CMD() {
        hackrf_transfer -t "$REC_FILE" -f "$FREQUENCY" -s "$SAMPLE_RATE" -x "$TX_GAIN" -a 1 2>&1
    }

    if [[ "$REPEAT_COUNT" -eq 0 ]]; then
        echo "Transmitting (continuous loop — Ctrl+C to stop)..."
        COUNT=1
        trap 'echo ""; echo "Stopped after ${COUNT} transmission(s)."; rm -f "$REC_FILE"; exit 0' INT
        while true; do
            echo "── Transmission #${COUNT} ──"
            REC_TX_CMD
            COUNT=$((COUNT + 1))
            sleep 0.5
        done
    elif [[ "$REPEAT_COUNT" -eq 1 ]]; then
        echo "Transmitting..."
        REC_TX_CMD
        echo "Transmission complete."
    else
        echo "Transmitting ${REPEAT_COUNT} times..."
        for ((i=1; i<=REPEAT_COUNT; i++)); do
            echo "── Transmission ${i}/${REPEAT_COUNT} ──"
            REC_TX_CMD
            [[ "$i" -lt "$REPEAT_COUNT" ]] && sleep 0.5
        done
        echo "All ${REPEAT_COUNT} transmissions complete."
    fi
    rm -f "$REC_FILE"
    exit 0
fi

if [[ "$TX_SOURCE" == "4" ]]; then
    # ── Text-to-speech transmit ──────────────────────────────────────────
    if ! command -v espeak-ng &>/dev/null; then
        echo ""
        echo "Error: 'espeak-ng' not found."
        echo "Install with: sudo apt install espeak-ng"
        exit 1
    fi

    echo ""
    echo "Select modulation for transmission:"
    echo "  1) NBFM (narrowband FM, +/-5 kHz)"
    echo "  2) WBFM (wideband FM, +/-75 kHz)"
    echo "  3) AM (amplitude modulation)"
    echo "  4) USB (upper sideband)"
    echo "  5) LSB (lower sideband)"
    read -rp "Enter choice [1-5]: " WAV_MOD
    case "$WAV_MOD" in
        1) WAV_MODE="WAV_NBFM"; WAV_LABEL="NBFM +/-5 kHz" ;;
        2) WAV_MODE="WAV_WBFM"; WAV_LABEL="WBFM +/-75 kHz" ;;
        3) WAV_MODE="WAV_AM";   WAV_LABEL="AM" ;;
        4) WAV_MODE="WAV_USB";  WAV_LABEL="USB" ;;
        5) WAV_MODE="WAV_LSB";  WAV_LABEL="LSB" ;;
        *) echo "Invalid."; exit 1 ;;
    esac

    echo ""
    echo "Enter message for text-to-speech (press Enter twice to finish):"
    TTS_MSG=""
    while IFS= read -r line; do
        [[ -z "$line" ]] && break
        [[ -n "$TTS_MSG" ]] && TTS_MSG="$TTS_MSG $line" || TTS_MSG="$line"
    done
    [[ -z "$TTS_MSG" ]] && { echo "Error: No message."; exit 1; }

    echo ""
    echo "Voice options (examples: en, en-us, en-gb, es, fr, de, ru, zh)"
    read -rp "Voice [en]: " TTS_VOICE
    TTS_VOICE="${TTS_VOICE:-en}"
    read -rp "Speed in words per minute [150]: " TTS_SPEED
    TTS_SPEED="${TTS_SPEED:-150}"
    read -rp "Word gap (pause between words, 1-50) [5]: " TTS_GAP
    TTS_GAP="${TTS_GAP:-5}"

    WAV_FILE=$(mktemp /tmp/hackrf_tts_XXXXXX.wav)
    echo "Generating speech..."
    espeak-ng -v "$TTS_VOICE" -s "$TTS_SPEED" -g "$TTS_GAP" -w "$WAV_FILE" "$TTS_MSG"
    if [[ ! -s "$WAV_FILE" ]]; then
        echo "Error: Speech generation failed."
        rm -f "$WAV_FILE"; exit 1
    fi

    echo ""
    echo "How many times to transmit?"
    echo "  Enter a number (e.g. 5), or 0 for continuous loop."
    echo "  Press Enter for a single transmission."
    read -rp "Repeat count [1]: " REPEAT_COUNT
    REPEAT_COUNT="${REPEAT_COUNT:-1}"
    if ! [[ "$REPEAT_COUNT" =~ ^[0-9]+$ ]]; then
        echo "Error: Invalid number."; rm -f "$WAV_FILE"; exit 1
    fi

    if [[ "$REPEAT_COUNT" -eq 0 ]]; then
        REPEAT_LABEL="continuous (Ctrl+C to stop)"
    else
        REPEAT_LABEL="${REPEAT_COUNT}"
    fi
    echo ""
    echo "========================================="
    echo " Frequency  : ${FREQ_MHZ} MHz"
    echo " Source     : TTS: ${TTS_MSG}"
    echo " Modulation : ${WAV_LABEL}"
    echo " TX Gain    : ${TX_GAIN} dB + RF amp"
    echo " Repeat     : ${REPEAT_LABEL}"
    echo "========================================="

    TTS_TX_CMD() {
        python3 "$SCRIPT_DIR/transmit_modes.py" "$WAV_MODE" "$WAV_FILE" \
            | hackrf_transfer -t - -f "$FREQUENCY" -s "$SAMPLE_RATE" -x "$TX_GAIN" -a 1 2>&1
    }

    if [[ "$REPEAT_COUNT" -eq 0 ]]; then
        echo "Transmitting (continuous loop — Ctrl+C to stop)..."
        COUNT=1
        trap 'echo ""; echo "Stopped after ${COUNT} transmission(s)."; rm -f "$WAV_FILE"; exit 0' INT
        while true; do
            echo "── Transmission #${COUNT} ──"
            TTS_TX_CMD
            COUNT=$((COUNT + 1))
            sleep 0.5
        done
    elif [[ "$REPEAT_COUNT" -eq 1 ]]; then
        echo "Transmitting..."
        TTS_TX_CMD
        echo "Transmission complete."
    else
        echo "Transmitting ${REPEAT_COUNT} times..."
        for ((i=1; i<=REPEAT_COUNT; i++)); do
            echo "── Transmission ${i}/${REPEAT_COUNT} ──"
            TTS_TX_CMD
            [[ "$i" -lt "$REPEAT_COUNT" ]] && sleep 0.5
        done
        echo "All ${REPEAT_COUNT} transmissions complete."
    fi
    rm -f "$WAV_FILE"
    exit 0
fi

if [[ "$TX_SOURCE" == "5" ]]; then
    # ── AI Voice Responder ───────────────────────────────────────────────
    # Pipeline: HackRF RX → demod → whisper → Claude API → espeak-ng → HackRF TX

    # Check dependencies
    WHISPER_BIN="$SCRIPT_DIR/whisper.cpp/main"
    WHISPER_MODELS="$SCRIPT_DIR/whisper.cpp/models"
    if [[ ! -x "$WHISPER_BIN" ]]; then
        echo ""
        echo "Error: whisper.cpp not found at $WHISPER_BIN"
        echo "Build it:"
        echo "  git clone https://github.com/ggerganov/whisper.cpp.git"
        echo "  cd whisper.cpp && git checkout v1.5.5 && make -j\$(nproc) main"
        echo "  bash models/download-ggml-model.sh base.en"
        exit 1
    fi
    if ! command -v espeak-ng &>/dev/null; then
        echo ""
        echo "Error: 'espeak-ng' not found."
        echo "Install with: sudo apt install espeak-ng"
        exit 1
    fi
    LLAMA_BIN="$SCRIPT_DIR/llama.cpp/llama-cli"
    LLAMA_MODEL_DIR="$SCRIPT_DIR/llama.cpp/models"
    LLAMA_MODEL_PATH="${LLAMA_MODEL_DIR}/qwen2.5-1.5b-instruct-q4_k_m.gguf"
    if [[ ! -x "$LLAMA_BIN" ]]; then
        echo ""
        echo "Error: llama.cpp not found at $LLAMA_BIN"
        echo "Build it:"
        echo "  git clone https://github.com/ggerganov/llama.cpp.git"
        echo "  cd llama.cpp && git checkout b4000 && make -j\$(nproc) llama-cli"
        exit 1
    fi
    if [[ ! -f "$LLAMA_MODEL_PATH" ]]; then
        echo ""
        echo "Error: LLM model not found at $LLAMA_MODEL_PATH"
        echo "Download it:"
        echo "  wget -O $LLAMA_MODEL_PATH \\"
        echo "    https://huggingface.co/Qwen/Qwen2.5-1.5B-Instruct-GGUF/resolve/main/qwen2.5-1.5b-instruct-q4_k_m.gguf"
        exit 1
    fi

    echo ""
    echo "Select receive/transmit modulation:"
    echo "  1) NBFM (narrowband FM)"
    echo "  2) WBFM (wideband FM)"
    echo "  3) AM"
    echo "  4) USB (upper sideband)"
    echo "  5) LSB (lower sideband)"
    read -rp "Enter choice [1-5]: " AI_MOD
    case "$AI_MOD" in
        1) AI_DEMOD="DEMOD_NBFM"; AI_TX_MODE="WAV_NBFM"; AI_LABEL="NBFM" ;;
        2) AI_DEMOD="DEMOD_WBFM"; AI_TX_MODE="WAV_WBFM"; AI_LABEL="WBFM" ;;
        3) AI_DEMOD="DEMOD_AM";   AI_TX_MODE="WAV_AM";   AI_LABEL="AM" ;;
        4) AI_DEMOD="DEMOD_USB";  AI_TX_MODE="WAV_USB";  AI_LABEL="USB" ;;
        5) AI_DEMOD="DEMOD_LSB";  AI_TX_MODE="WAV_LSB";  AI_LABEL="LSB" ;;
        *) echo "Invalid."; exit 1 ;;
    esac

    echo ""
    read -rp "Listen duration in seconds [5]: " LISTEN_SEC
    LISTEN_SEC="${LISTEN_SEC:-5}"
    if ! [[ "$LISTEN_SEC" =~ ^[0-9]+$ ]] || [[ "$LISTEN_SEC" -lt 1 ]]; then
        echo "Error: Invalid duration."; exit 1
    fi

    echo ""
    echo "RF receive gain:"
    read -rp "  LNA gain (0-40 dB, step 8) [16]: " LNA_GAIN
    LNA_GAIN="${LNA_GAIN:-16}"
    read -rp "  VGA gain (0-62 dB, step 2) [20]: " VGA_GAIN
    VGA_GAIN="${VGA_GAIN:-20}"

    echo ""
    echo "TTS voice options (examples: en, en-us, en-gb, es, fr, de)"
    read -rp "Voice [en]: " TTS_VOICE
    TTS_VOICE="${TTS_VOICE:-en}"
    read -rp "TTS speed in WPM [150]: " TTS_SPEED
    TTS_SPEED="${TTS_SPEED:-150}"

    echo ""
    echo "Whisper model (tiny.en, base.en, small.en, medium.en)"
    echo "  Models in: ${WHISPER_MODELS}/"
    read -rp "Model [base.en]: " WHISPER_MODEL
    WHISPER_MODEL="${WHISPER_MODEL:-base.en}"
    WHISPER_MODEL_PATH="${WHISPER_MODELS}/ggml-${WHISPER_MODEL}.bin"
    if [[ ! -f "$WHISPER_MODEL_PATH" ]]; then
        echo "  Model not found. Downloading ${WHISPER_MODEL}..."
        bash "${WHISPER_MODELS}/download-ggml-model.sh" "$WHISPER_MODEL"
        if [[ ! -f "$WHISPER_MODEL_PATH" ]]; then
            echo "Error: Failed to download model."; exit 1
        fi
    fi

    NUM_SAMPLES=$((SAMPLE_RATE * LISTEN_SEC))

    echo ""
    echo "========================================="
    echo " AI Voice Responder"
    echo " Frequency   : ${FREQ_MHZ} MHz"
    echo " Modulation  : ${AI_LABEL}"
    echo " Listen      : ${LISTEN_SEC}s"
    echo " RX Gain     : LNA ${LNA_GAIN} dB / VGA ${VGA_GAIN} dB"
    echo " TX Gain     : ${TX_GAIN} dB + RF amp"
    echo " Whisper     : ${WHISPER_MODEL}"
    echo " TTS Voice   : ${TTS_VOICE} @ ${TTS_SPEED} WPM"
    echo "========================================="
    echo ""
    echo "Entering AI responder loop (Ctrl+C to stop)..."
    echo ""

    ROUND=1
    trap 'echo ""; echo "AI responder stopped after $((ROUND - 1)) round(s)."; exit 0' INT

    while true; do
        echo "── Round ${ROUND}: Listening on ${FREQ_MHZ} MHz for ${LISTEN_SEC}s ──"

        # 1. Capture IQ
        RX_FILE=$(mktemp /tmp/hackrf_ai_rx_XXXXXX.raw)
        hackrf_transfer -r "$RX_FILE" -f "$FREQUENCY" -s "$SAMPLE_RATE" \
            -l "$LNA_GAIN" -g "$VGA_GAIN" -n "$NUM_SAMPLES" 2>&1

        if [[ ! -s "$RX_FILE" ]]; then
            echo "  No data captured, retrying..."
            rm -f "$RX_FILE"
            sleep 1
            ROUND=$((ROUND + 1))
            continue
        fi

        # 2. Demodulate IQ → WAV
        DEMOD_WAV=$(mktemp /tmp/hackrf_ai_demod_XXXXXX.wav)
        echo "  Demodulating..."
        python3 "$SCRIPT_DIR/transmit_modes.py" "$AI_DEMOD" "$RX_FILE" "$DEMOD_WAV"
        rm -f "$RX_FILE"

        if [[ ! -s "$DEMOD_WAV" ]]; then
            echo "  Demodulation produced no audio, retrying..."
            rm -f "$DEMOD_WAV"
            sleep 1
            ROUND=$((ROUND + 1))
            continue
        fi

        # 3. Transcribe with whisper.cpp
        echo "  Transcribing..."
        TRANSCRIPT=$("$WHISPER_BIN" \
            -m "$WHISPER_MODEL_PATH" \
            -f "$DEMOD_WAV" \
            --no-prints --no-timestamps \
            -l en 2>/dev/null | tr -s '[:space:]' ' ')
        rm -f "$DEMOD_WAV"

        # Skip if no speech detected
        TRIMMED=$(echo "$TRANSCRIPT" | tr -d '[:space:]')
        if [[ -z "$TRIMMED" ]]; then
            echo "  No speech detected, listening again..."
            ROUND=$((ROUND + 1))
            sleep 1
            continue
        fi

        echo "  Heard: ${TRANSCRIPT}"

        # 4. Generate response with local LLM
        echo "  Thinking..."
        PROMPT="<|im_start|>system
You are a helpful AI radio assistant. Keep responses concise, clear, and conversational. They will be spoken aloud via text-to-speech over radio. Limit to 2-3 sentences. Avoid special characters, URLs, and code.<|im_end|>
<|im_start|>user
${TRANSCRIPT}<|im_end|>
<|im_start|>assistant
"
        AI_TEXT=$("$LLAMA_BIN" \
            -m "$LLAMA_MODEL_PATH" \
            -p "$PROMPT" \
            -n 200 -c 512 --temp 0.7 \
            --no-display-prompt -e \
            --no-perf 2>/dev/null \
            | sed 's/<|im_end|>.*//' | sed 's/\[end of text\].*//')

        # Clean up: strip leading/trailing whitespace
        AI_TEXT=$(echo "$AI_TEXT" | sed '/^$/d' | head -10)
        AI_TEXT=$(echo "$AI_TEXT" | tr '\n' ' ' | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | tr -s ' ')

        if [[ -z "$AI_TEXT" ]]; then
            echo "  LLM produced no response, skipping..."
            ROUND=$((ROUND + 1))
            sleep 1
            continue
        fi

        echo "  AI: ${AI_TEXT}"

        # 5. TTS → WAV
        TTS_WAV=$(mktemp /tmp/hackrf_ai_tts_XXXXXX.wav)
        espeak-ng -v "$TTS_VOICE" -s "$TTS_SPEED" -w "$TTS_WAV" "$AI_TEXT"

        if [[ ! -s "$TTS_WAV" ]]; then
            echo "  TTS failed, skipping..."
            rm -f "$TTS_WAV"
            ROUND=$((ROUND + 1))
            sleep 1
            continue
        fi

        # 6. Modulate and transmit
        echo "  Transmitting response..."
        python3 "$SCRIPT_DIR/transmit_modes.py" "$AI_TX_MODE" "$TTS_WAV" \
            | hackrf_transfer -t - -f "$FREQUENCY" -s "$SAMPLE_RATE" -x "$TX_GAIN" -a 1 2>&1

        rm -f "$TTS_WAV"
        echo "  Response transmitted."
        echo ""

        ROUND=$((ROUND + 1))
        sleep 1
    done
    exit 0
fi

if [[ "$TX_SOURCE" == "6" ]]; then
    # ── Signal Analyzer / Decoder ─────────────────────────────────────────
    echo ""
    echo "Select demodulation mode for received signal:"
    echo "  1) NBFM (narrowband FM)"
    echo "  2) WBFM (wideband FM)"
    echo "  3) AM"
    echo "  4) USB (upper sideband)"
    echo "  5) LSB (lower sideband)"
    read -rp "Enter choice [1-5]: " SA_MOD
    case "$SA_MOD" in
        1) SA_DEMOD="DEMOD_NBFM"; SA_LABEL="NBFM" ;;
        2) SA_DEMOD="DEMOD_WBFM"; SA_LABEL="WBFM" ;;
        3) SA_DEMOD="DEMOD_AM";   SA_LABEL="AM" ;;
        4) SA_DEMOD="DEMOD_USB";  SA_LABEL="USB" ;;
        5) SA_DEMOD="DEMOD_LSB";  SA_LABEL="LSB" ;;
        *) echo "Invalid."; exit 1 ;;
    esac

    echo ""
    read -rp "Listen duration in seconds [10]: " LISTEN_SEC
    LISTEN_SEC="${LISTEN_SEC:-10}"
    if ! [[ "$LISTEN_SEC" =~ ^[0-9]+$ ]] || [[ "$LISTEN_SEC" -lt 1 ]]; then
        echo "Error: Invalid duration."; exit 1
    fi

    echo ""
    echo "RF receive gain:"
    read -rp "  LNA gain (0-40 dB, step 8) [16]: " LNA_GAIN
    LNA_GAIN="${LNA_GAIN:-16}"
    read -rp "  VGA gain (0-62 dB, step 2) [20]: " VGA_GAIN
    VGA_GAIN="${VGA_GAIN:-20}"

    echo ""
    echo "Select decode mode:"
    echo "  0) Auto-detect"
    echo "  1) CW (Morse code)"
    echo "  2) RTTY (45.45 baud, 170 Hz shift)"
    echo "  3) BPSK31"
    echo "  4) BPSK63"
    echo "  5) BPSK125"
    echo "  6) AFSK1200 (AX.25 / APRS)"
    echo "  7) MFSK16"
    echo "  8) MFSK32"
    echo "  9) MFSK64"
    echo " 10) Olivia 8/500"
    echo " 11) Olivia 16/500"
    echo " 12) Olivia 32/1000"
    echo " 13) FT8"
    read -rp "Enter choice [0-13]: " SA_DEC
    case "$SA_DEC" in
        0)  SA_DECODE="DECODE_AUTO";    DEC_LABEL="Auto-detect" ;;
        1)  SA_DECODE="DECODE_CW";      DEC_LABEL="CW / Morse" ;;
        2)  SA_DECODE="DECODE_RTTY";    DEC_LABEL="RTTY" ;;
        3)  SA_DECODE="DECODE_BPSK31";  DEC_LABEL="BPSK31" ;;
        4)  SA_DECODE="DECODE_BPSK63";  DEC_LABEL="BPSK63" ;;
        5)  SA_DECODE="DECODE_BPSK125"; DEC_LABEL="BPSK125" ;;
        6)  SA_DECODE="DECODE_AFSK1200";DEC_LABEL="AFSK1200 (AX.25/APRS)" ;;
        7)  SA_DECODE="DECODE_MFSK16";  DEC_LABEL="MFSK16" ;;
        8)  SA_DECODE="DECODE_MFSK32";  DEC_LABEL="MFSK32" ;;
        9)  SA_DECODE="DECODE_MFSK64";  DEC_LABEL="MFSK64" ;;
        10) SA_DECODE="DECODE_OLIVIA8"; DEC_LABEL="Olivia 8/500" ;;
        11) SA_DECODE="DECODE_OLIVIA16";DEC_LABEL="Olivia 16/500" ;;
        12) SA_DECODE="DECODE_OLIVIA32";DEC_LABEL="Olivia 32/1000" ;;
        13) SA_DECODE="DECODE_FT8";     DEC_LABEL="FT8" ;;
        *)  echo "Invalid."; exit 1 ;;
    esac

    NUM_SAMPLES=$((SAMPLE_RATE * LISTEN_SEC))

    echo ""
    echo "========================================="
    echo " Signal Analyzer / Decoder"
    echo " Frequency   : ${FREQ_MHZ} MHz"
    echo " Demod       : ${SA_LABEL}"
    echo " Decoder     : ${DEC_LABEL}"
    echo " Listen      : ${LISTEN_SEC}s"
    echo " RX Gain     : LNA ${LNA_GAIN} dB / VGA ${VGA_GAIN} dB"
    echo "========================================="
    echo ""
    echo "Entering signal analyzer loop (Ctrl+C to stop)..."
    echo ""

    ROUND=1
    trap 'echo ""; echo "Signal analyzer stopped after $((ROUND - 1)) round(s)."; exit 0' INT

    while true; do
        echo "── Round ${ROUND}: Listening on ${FREQ_MHZ} MHz for ${LISTEN_SEC}s ──"

        # 1. Capture IQ
        RX_FILE=$(mktemp /tmp/hackrf_sa_rx_XXXXXX.raw)
        hackrf_transfer -r "$RX_FILE" -f "$FREQUENCY" -s "$SAMPLE_RATE" \
            -l "$LNA_GAIN" -g "$VGA_GAIN" -n "$NUM_SAMPLES" 2>&1

        if [[ ! -s "$RX_FILE" ]]; then
            echo "  No data captured, retrying..."
            rm -f "$RX_FILE"
            sleep 1
            ROUND=$((ROUND + 1))
            continue
        fi

        # 2. Demodulate IQ → WAV
        DEMOD_WAV=$(mktemp /tmp/hackrf_sa_demod_XXXXXX.wav)
        echo "  Demodulating (${SA_LABEL})..."
        python3 "$SCRIPT_DIR/transmit_modes.py" "$SA_DEMOD" "$RX_FILE" "$DEMOD_WAV"
        rm -f "$RX_FILE"

        if [[ ! -s "$DEMOD_WAV" ]]; then
            echo "  Demodulation produced no audio, retrying..."
            rm -f "$DEMOD_WAV"
            sleep 1
            ROUND=$((ROUND + 1))
            continue
        fi

        # 3. Decode
        echo "  Decoding (${DEC_LABEL})..."
        DECODED=$(python3 "$SCRIPT_DIR/transmit_modes.py" "$SA_DECODE" "$DEMOD_WAV" 2>&1)
        rm -f "$DEMOD_WAV"

        # 4. Display result
        if [[ -n "$DECODED" ]]; then
            echo "  ┌─────────────────────────────────────"
            echo "$DECODED" | while IFS= read -r line; do
                echo "  │ $line"
            done
            echo "  └─────────────────────────────────────"
        else
            echo "  (no signal decoded)"
        fi

        echo ""
        ROUND=$((ROUND + 1))
        sleep 1
    done
    exit 0
fi

if [[ "$TX_SOURCE" == "7" ]]; then
    # ── Jitter Frequency Data Analysis ────────────────────────────────────
    # Captures RF, extracts peaks (1) and valleys (0) as binary,
    # then runs through ciphers, gematria, and math anomaly detection.
    echo ""
    echo "Select demodulation mode for received signal:"
    echo "  1) NBFM (narrowband FM)"
    echo "  2) WBFM (wideband FM)"
    echo "  3) AM"
    echo "  4) USB (upper sideband)"
    echo "  5) LSB (lower sideband)"
    read -rp "Enter choice [1-5]: " JF_MOD
    case "$JF_MOD" in
        1) JF_DEMOD="DEMOD_NBFM"; JF_LABEL="NBFM" ;;
        2) JF_DEMOD="DEMOD_WBFM"; JF_LABEL="WBFM" ;;
        3) JF_DEMOD="DEMOD_AM";   JF_LABEL="AM" ;;
        4) JF_DEMOD="DEMOD_USB";  JF_LABEL="USB" ;;
        5) JF_DEMOD="DEMOD_LSB";  JF_LABEL="LSB" ;;
        *) echo "Invalid."; exit 1 ;;
    esac

    echo ""
    read -rp "Listen duration in seconds [13.7]: " LISTEN_SEC
    LISTEN_SEC="${LISTEN_SEC:-13.7}"
    if ! [[ "$LISTEN_SEC" =~ ^[0-9]+\.?[0-9]*$ ]] || (( $(echo "$LISTEN_SEC < 0.1" | bc -l) )); then
        echo "Error: Invalid duration."; exit 1
    fi

    echo ""
    echo "RF receive gain:"
    read -rp "  LNA gain (0-40 dB, step 8) [16]: " LNA_GAIN
    LNA_GAIN="${LNA_GAIN:-16}"
    read -rp "  VGA gain (0-62 dB, step 2) [20]: " VGA_GAIN
    VGA_GAIN="${VGA_GAIN:-20}"

    NUM_SAMPLES=$(echo "$SAMPLE_RATE * $LISTEN_SEC / 1" | bc)

    echo ""
    echo "========================================="
    echo " Jitter Frequency Data Analysis"
    echo " Frequency   : ${FREQ_MHZ} MHz"
    echo " Demod       : ${JF_LABEL}"
    echo " Listen      : ${LISTEN_SEC}s"
    echo " RX Gain     : LNA ${LNA_GAIN} dB / VGA ${VGA_GAIN} dB"
    echo " Analysis    : Peaks→1, Valleys→0, Binary"
    echo "               Ciphers, Gematria, Math Anomalies"
    echo "========================================="
    echo ""
    echo "Entering jitter analysis loop (Ctrl+C to stop)..."
    echo "(All results auto-logged to anomaly repository)"
    echo ""

    # Start a logging session
    JF_SESSION=$(python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_SESSION_START \
        "$FREQ_MHZ" "$JF_LABEL" "Jitter frequency data")

    ROUND=1
    trap 'echo ""; echo "Jitter analyzer stopped after $((ROUND - 1)) round(s)."; exit 0' INT

    while true; do
        echo "══ Round ${ROUND}: Capturing on ${FREQ_MHZ} MHz for ${LISTEN_SEC}s ══"

        # 1. Capture IQ
        RX_FILE=$(mktemp /tmp/hackrf_jf_rx_XXXXXX.raw)
        hackrf_transfer -r "$RX_FILE" -f "$FREQUENCY" -s "$SAMPLE_RATE" \
            -l "$LNA_GAIN" -g "$VGA_GAIN" -n "$NUM_SAMPLES" 2>&1

        if [[ ! -s "$RX_FILE" ]]; then
            echo "  No data captured, retrying..."
            rm -f "$RX_FILE"
            sleep 1
            ROUND=$((ROUND + 1))
            continue
        fi

        # 2. Demodulate IQ → WAV
        DEMOD_WAV=$(mktemp /tmp/hackrf_jf_demod_XXXXXX.wav)
        echo "  Demodulating (${JF_LABEL})..."
        python3 "$SCRIPT_DIR/transmit_modes.py" "$JF_DEMOD" "$RX_FILE" "$DEMOD_WAV"
        rm -f "$RX_FILE"

        if [[ ! -s "$DEMOD_WAV" ]]; then
            echo "  Demodulation produced no audio, retrying..."
            rm -f "$DEMOD_WAV"
            sleep 1
            ROUND=$((ROUND + 1))
            continue
        fi

        # 3. Run full jitter frequency analysis (with auto-logging)
        echo "  Analyzing peaks/valleys → binary → ciphers/gematria/math..."
        echo ""
        python3 "$SCRIPT_DIR/transmit_modes.py" JITTER_ANALYZE "$DEMOD_WAV" \
            "$FREQ_MHZ" "$JF_LABEL" "$LISTEN_SEC" "$JF_SESSION"
        rm -f "$DEMOD_WAV"

        echo ""
        echo ""
        ROUND=$((ROUND + 1))
        sleep 2
    done
    exit 0
fi

if [[ "$TX_SOURCE" == "8" ]]; then
    # ── Anomaly Repository ────────────────────────────────────────────────
    LOG_DIR="$SCRIPT_DIR/hackrf_logs"

    while true; do
        echo ""
        echo "========================================="
        echo " Anomaly & Event Log Repository"
        echo "========================================="
        echo ""
        echo "  1) View all anomalies (most recent first)"
        echo "  2) View by category"
        echo "  3) View by severity"
        echo "  4) Search logs"
        echo "  5) Statistics dashboard"
        echo "  6) Export full report (text)"
        echo "  7) Export as JSON"
        echo "  8) Export as CSV"
        echo "  9) Archive & clear logs"
        echo "  0) Exit"
        echo ""
        read -rp "Enter choice [0-9]: " LOG_CHOICE

        case "$LOG_CHOICE" in
            1)
                echo ""
                echo "─── All Anomalies (most recent, max 50) ───"
                python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_QUERY _ ANOMALY _ 50
                echo ""
                read -rp "Press Enter to continue..." _
                ;;
            2)
                echo ""
                echo "Select category:"
                echo "  1) SYSTEM   — captures, sessions, demod events"
                echo "  2) SIGNAL   — signal detection, mode identification"
                echo "  3) CIPHER   — Caesar, Atbash, XOR, Bacon, ASCII"
                echo "  4) GEMATRIA — Hebrew, English, Simple, Abjad, Greek"
                echo "  5) MATH     — Pi, Phi, Fibonacci, primes, entropy"
                echo "  6) WORD     — word/sentence detection"
                echo "  7) PATTERN  — repeating patterns, palindromes"
                read -rp "Enter choice [1-7]: " CAT_CHOICE
                case "$CAT_CHOICE" in
                    1) QCAT="SYSTEM" ;;
                    2) QCAT="SIGNAL" ;;
                    3) QCAT="CIPHER" ;;
                    4) QCAT="GEMATRIA" ;;
                    5) QCAT="MATH" ;;
                    6) QCAT="WORD" ;;
                    7) QCAT="PATTERN" ;;
                    *) echo "Invalid."; continue ;;
                esac
                echo ""
                echo "─── ${QCAT} Events ───"
                python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_QUERY "$QCAT" _ _ 50
                echo ""
                read -rp "Press Enter to continue..." _
                ;;
            3)
                echo ""
                echo "Select severity:"
                echo "  1) CRITICAL"
                echo "  2) ANOMALY"
                echo "  3) NOTABLE"
                echo "  4) INFO"
                read -rp "Enter choice [1-4]: " SEV_CHOICE
                case "$SEV_CHOICE" in
                    1) QSEV="CRITICAL" ;;
                    2) QSEV="ANOMALY" ;;
                    3) QSEV="NOTABLE" ;;
                    4) QSEV="INFO" ;;
                    *) echo "Invalid."; continue ;;
                esac
                echo ""
                echo "─── ${QSEV} Events ───"
                python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_QUERY _ "$QSEV" _ 50
                echo ""
                read -rp "Press Enter to continue..." _
                ;;
            4)
                echo ""
                read -rp "Enter search term: " SEARCH_TERM
                if [[ -n "$SEARCH_TERM" ]]; then
                    echo ""
                    echo "─── Search: '${SEARCH_TERM}' ───"
                    python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_QUERY _ _ "$SEARCH_TERM" 50
                fi
                echo ""
                read -rp "Press Enter to continue..." _
                ;;
            5)
                echo ""
                echo "═══════════════════════════════════════════"
                echo " Statistics Dashboard"
                echo "═══════════════════════════════════════════"
                python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_STATS
                echo ""
                read -rp "Press Enter to continue..." _
                ;;
            6)
                EXPORT_FILE="$LOG_DIR/export_$(date +%Y%m%d_%H%M%S).txt"
                mkdir -p "$LOG_DIR"
                python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_EXPORT text "$EXPORT_FILE"
                echo "Exported to: $EXPORT_FILE"
                echo ""
                read -rp "Also display on screen? [y/N]: " SHOW_EXPORT
                if [[ "$SHOW_EXPORT" =~ ^[Yy] ]]; then
                    cat "$EXPORT_FILE"
                fi
                echo ""
                read -rp "Press Enter to continue..." _
                ;;
            7)
                EXPORT_FILE="$LOG_DIR/export_$(date +%Y%m%d_%H%M%S).json"
                mkdir -p "$LOG_DIR"
                python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_EXPORT json "$EXPORT_FILE"
                echo "Exported to: $EXPORT_FILE"
                echo ""
                read -rp "Press Enter to continue..." _
                ;;
            8)
                EXPORT_FILE="$LOG_DIR/export_$(date +%Y%m%d_%H%M%S).csv"
                mkdir -p "$LOG_DIR"
                python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_EXPORT csv "$EXPORT_FILE"
                echo "Exported to: $EXPORT_FILE"
                echo ""
                read -rp "Press Enter to continue..." _
                ;;
            9)
                echo ""
                read -rp "Archive current logs before clearing? [Y/n]: " ARCHIVE_CHOICE
                if [[ "$ARCHIVE_CHOICE" =~ ^[Nn] ]]; then
                    read -rp "Are you sure? This will permanently delete all logs. [y/N]: " CONFIRM
                    if [[ "$CONFIRM" =~ ^[Yy] ]]; then
                        python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_CLEAR no_archive
                    else
                        echo "Cancelled."
                    fi
                else
                    python3 "$SCRIPT_DIR/transmit_modes.py" LOGSTORE_CLEAR
                fi
                echo ""
                read -rp "Press Enter to continue..." _
                ;;
            0)
                echo "Exiting repository."
                exit 0
                ;;
            *)
                echo "Invalid choice."
                ;;
        esac
    done
    exit 0
fi

# ── Step 3: Mode Category ─────────────────────────────────────────────────
echo ""
echo "Select mode category:"
echo "  1) CW / Morse Code"
echo "  2) PSK Modes"
echo "  3) FSK / RTTY"
echo "  4) MFSK"
echo "  5) Olivia"
echo "  6) Weak Signal (FT8/FT4/WSPR/JT65)"
echo "  7) Analog (AM/NBFM/WBFM/SSB)"
echo "  8) Packet / Data (AX.25/APRS)"
echo "  9) THOR (IFK+ MFSK)"
read -rp "Enter choice [1-9]: " CAT

case "$CAT" in
    1) # CW / Morse
        echo ""
        echo "  1) AM carrier"
        echo "  2) FM carrier"
        read -rp "Enter choice [1-2]: " CW_MOD
        case "$CW_MOD" in
            1) MODE="CW_AM"; MODE_LABEL="CW / Morse Code (AM)" ;;
            2) MODE="CW_FM"; MODE_LABEL="CW / Morse Code (FM)" ;;
            *) echo "Invalid."; exit 1 ;;
        esac
        ;;
    2) # PSK
        echo ""
        echo "  1) BPSK31    (31.25 baud, 1 bit/sym)"
        echo "  2) BPSK63    (62.5 baud, 1 bit/sym)"
        echo "  3) BPSK125   (125 baud, 1 bit/sym)"
        echo "  4) QPSK31    (31.25 baud, 2 bit/sym)"
        echo "  5) QPSK63    (62.5 baud, 2 bit/sym)"
        echo "  6) 8PSK125   (125 baud, 3 bit/sym)"
        echo "  7) 8PSK250   (250 baud, 3 bit/sym)"
        echo "  8) 8PSK500   (500 baud, 3 bit/sym)"
        echo "  9) 8PSK1200F (1200 baud, 3 bit/sym, RRC)"
        read -rp "Enter choice [1-9]: " PSK
        case "$PSK" in
            1) MODE="BPSK31";    MODE_LABEL="BPSK31 (31.25 baud)" ;;
            2) MODE="BPSK63";    MODE_LABEL="BPSK63 (62.5 baud)" ;;
            3) MODE="BPSK125";   MODE_LABEL="BPSK125 (125 baud)" ;;
            4) MODE="QPSK31";    MODE_LABEL="QPSK31 (31.25 baud)" ;;
            5) MODE="QPSK63";    MODE_LABEL="QPSK63 (62.5 baud)" ;;
            6) MODE="8PSK125";   MODE_LABEL="8PSK125 (125 baud)" ;;
            7) MODE="8PSK250";   MODE_LABEL="8PSK250 (250 baud)" ;;
            8) MODE="8PSK500";   MODE_LABEL="8PSK500 (500 baud)" ;;
            9) MODE="8PSK1200F"; MODE_LABEL="8PSK1200F (1200 baud)" ;;
            *) echo "Invalid."; exit 1 ;;
        esac
        ;;
    3) # FSK / RTTY
        echo ""
        echo "  1) RTTY  (45.45 baud, 170 Hz shift)"
        echo "  2) RTTY  (50 baud, 170 Hz shift)"
        echo "  3) FSK441 (meteor scatter, 441 baud)"
        echo "  4) AFSK1200 (Bell 202, 1200 baud)"
        echo "  5) AFSK2400 (2400 baud)"
        read -rp "Enter choice [1-5]: " FSK
        case "$FSK" in
            1) MODE="RTTY45";   MODE_LABEL="RTTY (45.45 baud, 170 Hz)" ;;
            2) MODE="RTTY50";   MODE_LABEL="RTTY (50 baud, 170 Hz)" ;;
            3) MODE="FSK441";   MODE_LABEL="FSK441 (441 baud, 4-tone)" ;;
            4) MODE="AFSK1200"; MODE_LABEL="AFSK1200 (Bell 202)" ;;
            5) MODE="AFSK2400"; MODE_LABEL="AFSK2400 (2400 baud)" ;;
            *) echo "Invalid."; exit 1 ;;
        esac
        ;;
    4) # MFSK
        echo ""
        echo "  1) MFSK16 (16 tones, 15.625 baud)"
        echo "  2) MFSK32 (32 tones, 31.25 baud)"
        echo "  3) MFSK64 (64 tones, 62.5 baud)"
        read -rp "Enter choice [1-3]: " MF
        case "$MF" in
            1) MODE="MFSK16"; MODE_LABEL="MFSK16 (16 tones)" ;;
            2) MODE="MFSK32"; MODE_LABEL="MFSK32 (32 tones)" ;;
            3) MODE="MFSK64"; MODE_LABEL="MFSK64 (64 tones)" ;;
            *) echo "Invalid."; exit 1 ;;
        esac
        ;;
    5) # Olivia
        echo ""
        echo "  1) Olivia 8/500   (8 tones, 500 Hz BW)"
        echo "  2) Olivia 16/500  (16 tones, 500 Hz BW)"
        echo "  3) Olivia 32/1000 (32 tones, 1000 Hz BW)"
        read -rp "Enter choice [1-3]: " OL
        case "$OL" in
            1) MODE="OLIVIA8";  MODE_LABEL="Olivia 8/500" ;;
            2) MODE="OLIVIA16"; MODE_LABEL="Olivia 16/500" ;;
            3) MODE="OLIVIA32"; MODE_LABEL="Olivia 32/1000" ;;
            *) echo "Invalid."; exit 1 ;;
        esac
        ;;
    6) # Weak Signal
        echo ""
        echo "  1) FT8   (8-tone GFSK, 6.25 baud)"
        echo "  2) FT4   (4-tone GFSK, 12.5 baud)"
        echo "  3) WSPR  (4-tone FSK, 1.46 baud)"
        echo "  4) JT65  (65-tone FSK, 2.69 baud)"
        echo ""
        echo "  Note: Simplified encoding. For standard-"
        echo "  compatible FT8/WSPR/JT65, use WSJT-X."
        read -rp "Enter choice [1-4]: " WS
        case "$WS" in
            1) MODE="FT8";  MODE_LABEL="FT8 (8-GFSK, 6.25 baud)" ;;
            2) MODE="FT4";  MODE_LABEL="FT4 (4-GFSK, 12.5 baud)" ;;
            3) MODE="WSPR"; MODE_LABEL="WSPR (4-FSK, 1.46 baud)" ;;
            4) MODE="JT65"; MODE_LABEL="JT65 (65-FSK, 2.69 baud)" ;;
            *) echo "Invalid."; exit 1 ;;
        esac
        ;;
    7) # Analog
        echo ""
        echo "  1) AM   (amplitude modulation)"
        echo "  2) NBFM (narrowband FM, +/-5 kHz)"
        echo "  3) WBFM (wideband FM, +/-75 kHz)"
        echo "  4) USB  (upper sideband)"
        echo "  5) LSB  (lower sideband)"
        echo ""
        echo "  Message will be Morse-encoded as audio."
        read -rp "Enter choice [1-5]: " AN
        case "$AN" in
            1) MODE="AM";   MODE_LABEL="AM (Morse audio)" ;;
            2) MODE="NBFM"; MODE_LABEL="NBFM +/-5 kHz (Morse audio)" ;;
            3) MODE="WBFM"; MODE_LABEL="WBFM +/-75 kHz (Morse audio)" ;;
            4) MODE="USB";  MODE_LABEL="USB (Morse audio)" ;;
            5) MODE="LSB";  MODE_LABEL="LSB (Morse audio)" ;;
            *) echo "Invalid."; exit 1 ;;
        esac
        ;;
    8) # Packet / Data
        echo ""
        echo "  1) AX.25  (packet radio, AFSK1200)"
        echo "  2) APRS   (APRS beacon, AFSK1200)"
        read -rp "Enter choice [1-2]: " PK
        case "$PK" in
            1) MODE="AX25"; MODE_LABEL="AX.25 Packet (AFSK1200)" ;;
            2) MODE="APRS"; MODE_LABEL="APRS Beacon (AFSK1200)" ;;
            *) echo "Invalid."; exit 1 ;;
        esac
        echo ""
        read -rp "Enter your callsign (default N0CALL): " CS
        [[ -n "$CS" ]] && CALLSIGN="$CS"
        ;;
    9) # THOR
        MODE="THOR100"; MODE_LABEL="THOR 100 (64-tone IFK+, 100 baud, ~6400 Hz BW)"
        ;;
    *)
        echo "Invalid category."
        exit 1
        ;;
esac

# ── Step 3: Message ────────────────────────────────────────────────────────
echo ""
echo "Enter message to transmit (press Enter twice to finish):"
MESSAGE=""
while IFS= read -r line; do
    [[ -z "$line" ]] && break
    [[ -n "$MESSAGE" ]] && MESSAGE="$MESSAGE
$line" || MESSAGE="$line"
done
[[ -z "$MESSAGE" ]] && { echo "Error: No message."; exit 1; }

# ── Step 4: Repeat Count ──────────────────────────────────────────────────
echo ""
echo "How many times to transmit?"
echo "  Enter a number (e.g. 5), or 0 for continuous loop."
echo "  Press Enter for a single transmission."
read -rp "Repeat count [1]: " REPEAT_COUNT
REPEAT_COUNT="${REPEAT_COUNT:-1}"
if ! [[ "$REPEAT_COUNT" =~ ^[0-9]+$ ]]; then
    echo "Error: Invalid number."; exit 1
fi

# ── Summary ────────────────────────────────────────────────────────────────
if [[ "$REPEAT_COUNT" -eq 0 ]]; then
    REPEAT_LABEL="continuous (Ctrl+C to stop)"
else
    REPEAT_LABEL="${REPEAT_COUNT}"
fi
echo ""
echo "========================================="
echo " Frequency : ${FREQ_MHZ} MHz"
echo " Mode      : ${MODE_LABEL}"
echo " TX Gain   : ${TX_GAIN} dB + RF amp"
echo " Message   : ${MESSAGE}"
[[ "$MODE" == "AX25" || "$MODE" == "APRS" ]] && echo " Callsign  : ${CALLSIGN}"
echo " Repeat    : ${REPEAT_LABEL}"
echo "========================================="

TX_CMD() {
    python3 "$SCRIPT_DIR/transmit_modes.py" \
        "$MODE" "$MESSAGE" "$WPM" "$TONE_FREQ" "$F_DEV" "$CALLSIGN" \
        | hackrf_transfer -t - -f "$FREQUENCY" -s "$SAMPLE_RATE" -x "$TX_GAIN" -a 1 -x 47 2>&1
}

if [[ "$REPEAT_COUNT" -eq 0 ]]; then
    # Continuous loop
    echo "Transmitting (continuous loop — Ctrl+C to stop)..."
    COUNT=1
    trap 'echo ""; echo "Stopped after ${COUNT} transmission(s)."; exit 0' INT
    while true; do
        echo "── Transmission #${COUNT} ──"
        TX_CMD
        COUNT=$((COUNT + 1))
        sleep 0.5
    done
elif [[ "$REPEAT_COUNT" -eq 1 ]]; then
    echo "Transmitting..."
    TX_CMD
    echo "Transmission complete."
else
    echo "Transmitting ${REPEAT_COUNT} times..."
    for ((i=1; i<=REPEAT_COUNT; i++)); do
        echo "── Transmission ${i}/${REPEAT_COUNT} ──"
        TX_CMD
        [[ "$i" -lt "$REPEAT_COUNT" ]] && sleep 0.5
    done
    echo "All ${REPEAT_COUNT} transmissions complete."
fi
