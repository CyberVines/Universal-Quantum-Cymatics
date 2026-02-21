#!/usr/bin/env python3
"""UQC CYBERVINES.COM Multi-Mode Transmitter — FastAPI Web Backend."""

import asyncio
import os
import re
import shlex
import tempfile
import time
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, field_validator

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent.parent  # UQC root
TRANSMIT_PY = SCRIPT_DIR / "transmit_modes.py"
SAMPLE_RATE = 8_000_000

# ── Whitelist constants ──────────────────────────────────────────────────────
VALID_TX_MODES = {
    "CW_AM", "CW_FM",
    "BPSK31", "BPSK63", "BPSK125", "QPSK31", "QPSK63",
    "8PSK125", "8PSK250", "8PSK500", "8PSK1200F",
    "RTTY45", "RTTY50", "FSK441", "AFSK1200", "AFSK2400",
    "MFSK16", "MFSK32", "MFSK64",
    "OLIVIA8", "OLIVIA16", "OLIVIA32",
    "FT8", "FT4", "WSPR", "JT65",
    "AM", "NBFM", "WBFM", "USB", "LSB",
    "AX25", "APRS",
    "THOR100",
    "MUSIC_CIPHER",
}

VALID_WAV_MODES = {"WAV_NBFM", "WAV_WBFM", "WAV_AM", "WAV_USB", "WAV_LSB"}

VALID_DEMOD_MODES = {"DEMOD_NBFM", "DEMOD_WBFM", "DEMOD_AM", "DEMOD_USB", "DEMOD_LSB"}

VALID_DECODE_MODES = {
    "DECODE_AUTO", "DECODE_CW", "DECODE_RTTY",
    "DECODE_BPSK31", "DECODE_BPSK63", "DECODE_BPSK125",
    "DECODE_AFSK1200",
    "DECODE_MFSK16", "DECODE_MFSK32", "DECODE_MFSK64",
    "DECODE_OLIVIA8", "DECODE_OLIVIA16", "DECODE_OLIVIA32",
    "DECODE_FT8", "DECODE_MUSIC_CIPHER",
}

VALID_VOICES = {
    "en", "en-us", "en-gb", "es", "fr", "de", "ru", "zh", "ja",
    "it", "pt", "nl", "pl", "ko", "ar", "hi", "tr", "sv",
}

VALID_WHISPER_MODELS = {"tiny.en", "base.en", "small.en", "medium.en"}

VALID_LOG_CATEGORIES = {"_", "SYSTEM", "SIGNAL", "CIPHER", "GEMATRIA", "MATH", "WORD", "PATTERN", "MUSIC"}
VALID_LOG_SEVERITIES = {"_", "CRITICAL", "ANOMALY", "NOTABLE", "INFO"}
VALID_EXPORT_FORMATS = {"text", "json", "csv"}

# Callsign: alphanumeric + dash/slash only, max 10 chars
CALLSIGN_RE = re.compile(r'^[A-Za-z0-9/\-]{1,10}$')


def _validate_callsign(v: str) -> str:
    if not CALLSIGN_RE.match(v):
        raise ValueError("Callsign must be 1-10 alphanumeric characters")
    return v.upper()


# ── App ──────────────────────────────────────────────────────────────────────
app = FastAPI(title="UQC CYBERVINES.COM Multi-Mode TX/RX")

# ── Process tracking ─────────────────────────────────────────────────────────
active_processes: dict[str, asyncio.subprocess.Process] = {}


async def kill_process(key: str) -> bool:
    proc = active_processes.pop(key, None)
    if proc and proc.returncode is None:
        try:
            proc.terminate()
            await asyncio.wait_for(proc.wait(), timeout=3)
        except (ProcessLookupError, asyncio.TimeoutError):
            try:
                proc.kill()
            except ProcessLookupError:
                pass
        return True
    return False


# ── Mode definitions ─────────────────────────────────────────────────────────
MODE_CATEGORIES = [
    {
        "id": 1, "name": "CW / Morse Code", "icon": "morse",
        "modes": [
            {"id": "CW_AM", "label": "AM carrier"},
            {"id": "CW_FM", "label": "FM carrier"},
        ]
    },
    {
        "id": 2, "name": "PSK Modes", "icon": "psk",
        "modes": [
            {"id": "BPSK31", "label": "BPSK31 (31.25 baud)"},
            {"id": "BPSK63", "label": "BPSK63 (62.5 baud)"},
            {"id": "BPSK125", "label": "BPSK125 (125 baud)"},
            {"id": "QPSK31", "label": "QPSK31 (31.25 baud)"},
            {"id": "QPSK63", "label": "QPSK63 (62.5 baud)"},
            {"id": "8PSK125", "label": "8PSK125 (125 baud)"},
            {"id": "8PSK250", "label": "8PSK250 (250 baud)"},
            {"id": "8PSK500", "label": "8PSK500 (500 baud)"},
            {"id": "8PSK1200F", "label": "8PSK1200F (1200 baud, RRC)"},
        ]
    },
    {
        "id": 3, "name": "FSK / RTTY", "icon": "fsk",
        "modes": [
            {"id": "RTTY45", "label": "RTTY (45.45 baud, 170 Hz)"},
            {"id": "RTTY50", "label": "RTTY (50 baud, 170 Hz)"},
            {"id": "FSK441", "label": "FSK441 (441 baud, 4-tone)"},
            {"id": "AFSK1200", "label": "AFSK1200 (Bell 202)"},
            {"id": "AFSK2400", "label": "AFSK2400 (2400 baud)"},
        ]
    },
    {
        "id": 4, "name": "MFSK", "icon": "mfsk",
        "modes": [
            {"id": "MFSK16", "label": "MFSK16 (16 tones)"},
            {"id": "MFSK32", "label": "MFSK32 (32 tones)"},
            {"id": "MFSK64", "label": "MFSK64 (64 tones)"},
        ]
    },
    {
        "id": 5, "name": "Olivia", "icon": "olivia",
        "modes": [
            {"id": "OLIVIA8", "label": "Olivia 8/500"},
            {"id": "OLIVIA16", "label": "Olivia 16/500"},
            {"id": "OLIVIA32", "label": "Olivia 32/1000"},
        ]
    },
    {
        "id": 6, "name": "Weak Signal", "icon": "weak",
        "modes": [
            {"id": "FT8", "label": "FT8 (8-GFSK, 6.25 baud)"},
            {"id": "FT4", "label": "FT4 (4-GFSK, 12.5 baud)"},
            {"id": "WSPR", "label": "WSPR (4-FSK, 1.46 baud)"},
            {"id": "JT65", "label": "JT65 (65-FSK, 2.69 baud)"},
        ]
    },
    {
        "id": 7, "name": "Analog", "icon": "analog",
        "modes": [
            {"id": "AM", "label": "AM (Morse audio)"},
            {"id": "NBFM", "label": "NBFM +/-5 kHz"},
            {"id": "WBFM", "label": "WBFM +/-75 kHz"},
            {"id": "USB", "label": "USB (upper sideband)"},
            {"id": "LSB", "label": "LSB (lower sideband)"},
        ]
    },
    {
        "id": 8, "name": "Packet / Data", "icon": "packet",
        "modes": [
            {"id": "AX25", "label": "AX.25 Packet (AFSK1200)"},
            {"id": "APRS", "label": "APRS Beacon (AFSK1200)"},
        ]
    },
    {
        "id": 9, "name": "THOR", "icon": "thor",
        "modes": [
            {"id": "THOR100", "label": "THOR 100 (64-tone IFK+, 100 baud)"},
        ]
    },
    {
        "id": 10, "name": "Musical Cipher", "icon": "music",
        "modes": [
            {"id": "MUSIC_CIPHER", "label": "Chromatic (A=C4 ... Z=C#6)"},
        ],
        "note": "A=C4 B=C#4 ... L=B4 | M=C5 ... X=B5 | Y=C6 Z=C#6"
    },
]


# ── Pydantic models with validation ─────────────────────────────────────────
class TransmitRequest(BaseModel):
    mode: str
    message: str
    frequency: float  # MHz
    wpm: int = 43
    tone_freq: int = 572
    f_dev: int = 5000
    callsign: str = "N0CALL"
    tx_gain: int = 47
    repeat: int = 1  # 0 = continuous

    @field_validator("mode")
    @classmethod
    def mode_must_be_valid(cls, v):
        if v not in VALID_TX_MODES:
            raise ValueError(f"Invalid mode: {v}")
        return v

    @field_validator("frequency")
    @classmethod
    def freq_in_range(cls, v):
        if not 0.1 <= v <= 7250:
            raise ValueError("Frequency must be 0.1–7250 MHz")
        return v

    @field_validator("tx_gain")
    @classmethod
    def gain_in_range(cls, v):
        if not 0 <= v <= 47:
            raise ValueError("TX gain must be 0–47")
        return v

    @field_validator("callsign")
    @classmethod
    def callsign_valid(cls, v):
        return _validate_callsign(v)


class RawTransmitRequest(BaseModel):
    file_path: str
    frequency: float  # MHz
    tx_gain: int = 47
    repeat: int = 1

    @field_validator("frequency")
    @classmethod
    def freq_in_range(cls, v):
        if not 0.1 <= v <= 7250:
            raise ValueError("Frequency must be 0.1–7250 MHz")
        return v


class TTSRequest(BaseModel):
    message: str
    frequency: float  # MHz
    modulation: str = "WAV_NBFM"
    voice: str = "en"
    speed: int = 150
    word_gap: int = 5
    tx_gain: int = 47
    repeat: int = 1

    @field_validator("modulation")
    @classmethod
    def mod_must_be_valid(cls, v):
        if v not in VALID_WAV_MODES:
            raise ValueError(f"Invalid modulation: {v}")
        return v

    @field_validator("voice")
    @classmethod
    def voice_must_be_valid(cls, v):
        if v not in VALID_VOICES:
            raise ValueError(f"Invalid voice: {v}")
        return v

    @field_validator("frequency")
    @classmethod
    def freq_in_range(cls, v):
        if not 0.1 <= v <= 7250:
            raise ValueError("Frequency must be 0.1–7250 MHz")
        return v


class ExportRequest(BaseModel):
    format: str = "text"

    @field_validator("format")
    @classmethod
    def format_must_be_valid(cls, v):
        if v not in VALID_EXPORT_FORMATS:
            raise ValueError(f"Invalid format: {v}")
        return v


class ClearRequest(BaseModel):
    no_archive: bool = False


# ── Helper: build a safe shell pipeline for TX ───────────────────────────────
def _build_tx_pipeline(mode: str, message: str, wpm: int, tone: int,
                       fdev: int, callsign: str, freq_hz: int,
                       tx_gain: int) -> str:
    """Build a shell command string with all values safely quoted."""
    return (
        f"python3 {shlex.quote(str(TRANSMIT_PY))} "
        f"{shlex.quote(mode)} {shlex.quote(message)} "
        f"{int(wpm)} {int(tone)} {int(fdev)} {shlex.quote(callsign)} "
        f"| hackrf_transfer -t - -f {int(freq_hz)} -s {SAMPLE_RATE} "
        f"-x {int(tx_gain)} -a 1"
    )


def _build_wav_tx_pipeline(wav_mode: str, wav_path: str,
                           freq_hz: int, tx_gain: int) -> str:
    """Build a shell pipeline for WAV modulation + transmit."""
    return (
        f"python3 {shlex.quote(str(TRANSMIT_PY))} "
        f"{shlex.quote(wav_mode)} {shlex.quote(wav_path)} "
        f"| hackrf_transfer -t - -f {int(freq_hz)} -s {SAMPLE_RATE} "
        f"-x {int(tx_gain)} -a 1"
    )


# ── REST Endpoints ───────────────────────────────────────────────────────────

@app.get("/api/status")
async def get_status():
    """Check HackRF hardware and active processes."""
    hackrf_found = False
    hackrf_info = ""
    try:
        proc = await asyncio.create_subprocess_exec(
            "hackrf_info",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=5)
        hackrf_found = proc.returncode == 0
        hackrf_info = stdout.decode(errors="replace").strip()
    except (FileNotFoundError, asyncio.TimeoutError):
        pass

    return {
        "hackrf_detected": hackrf_found,
        "hackrf_info": hackrf_info,
        "active_processes": {k: (v.returncode is None) for k, v in active_processes.items()},
        "transmit_modes_available": TRANSMIT_PY.exists(),
    }


@app.get("/api/modes")
async def get_modes():
    """Return all mode categories and sub-options."""
    return {"categories": MODE_CATEGORIES}


@app.post("/api/transmit")
async def start_transmit(req: TransmitRequest):
    """Start a transmission."""
    await kill_process("transmit")

    freq_hz = int(req.frequency * 1_000_000)
    cmd = _build_tx_pipeline(
        req.mode, req.message, req.wpm, req.tone_freq,
        req.f_dev, req.callsign, freq_hz, req.tx_gain,
    )

    async def run_tx():
        iterations = req.repeat if req.repeat > 0 else 999_999
        for i in range(iterations):
            if "transmit" not in active_processes:
                break
            proc = await asyncio.create_subprocess_exec(
                "bash", "-c", cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            active_processes["transmit"] = proc
            await proc.wait()
            if req.repeat > 0 and i + 1 >= req.repeat:
                break
            if "transmit" in active_processes:
                await asyncio.sleep(0.5)
        active_processes.pop("transmit", None)

    # Register a sentinel so the loop's "transmit" in active_processes check passes
    sentinel = await asyncio.create_subprocess_exec("true")
    active_processes["transmit"] = sentinel
    asyncio.create_task(run_tx())

    return {
        "status": "transmitting",
        "mode": req.mode,
        "frequency_mhz": req.frequency,
        "repeat": req.repeat,
    }


@app.post("/api/transmit/stop")
async def stop_transmit():
    """Stop active transmission."""
    killed = await kill_process("transmit")
    return {"status": "stopped" if killed else "no_active_transmission"}


@app.post("/api/transmit/raw")
async def transmit_raw(req: RawTransmitRequest):
    """Transmit a raw IQ file."""
    file_path = os.path.expanduser(req.file_path)
    if not os.path.isfile(file_path):
        return JSONResponse(status_code=400, content={"error": f"File not found: {file_path}"})

    await kill_process("transmit")
    freq_hz = int(req.frequency * 1_000_000)

    file_size = os.path.getsize(file_path)
    duration = file_size / (SAMPLE_RATE * 2)

    async def run_raw():
        iterations = req.repeat if req.repeat > 0 else 999_999
        for i in range(iterations):
            if "transmit" not in active_processes:
                break
            proc = await asyncio.create_subprocess_exec(
                "hackrf_transfer", "-t", file_path,
                "-f", str(freq_hz), "-s", str(SAMPLE_RATE),
                "-x", str(req.tx_gain), "-a", "1",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            active_processes["transmit"] = proc
            await proc.wait()
            if req.repeat > 0 and i + 1 >= req.repeat:
                break
            if "transmit" in active_processes:
                await asyncio.sleep(0.5)
        active_processes.pop("transmit", None)

    sentinel = await asyncio.create_subprocess_exec("true")
    active_processes["transmit"] = sentinel
    asyncio.create_task(run_raw())

    return {
        "status": "transmitting",
        "file": file_path,
        "file_size": file_size,
        "duration_sec": round(duration, 2),
        "frequency_mhz": req.frequency,
        "repeat": req.repeat,
    }


@app.post("/api/tts")
async def tts_transmit(req: TTSRequest):
    """Text-to-speech transmit."""
    await kill_process("transmit")

    wav_fd, wav_file = tempfile.mkstemp(suffix=".wav", prefix="hackrf_tts_")
    os.close(wav_fd)
    freq_hz = int(req.frequency * 1_000_000)

    # Generate speech
    tts_proc = await asyncio.create_subprocess_exec(
        "espeak-ng", "-v", req.voice, "-s", str(req.speed),
        "-g", str(req.word_gap), "-w", wav_file, req.message,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    await tts_proc.wait()

    if not os.path.isfile(wav_file) or os.path.getsize(wav_file) == 0:
        _try_unlink(wav_file)
        return JSONResponse(status_code=500, content={"error": "TTS generation failed"})

    cmd = _build_wav_tx_pipeline(req.modulation, wav_file, freq_hz, req.tx_gain)

    async def run_tts():
        iterations = req.repeat if req.repeat > 0 else 999_999
        for i in range(iterations):
            if "transmit" not in active_processes:
                break
            proc = await asyncio.create_subprocess_exec(
                "bash", "-c", cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            active_processes["transmit"] = proc
            await proc.wait()
            if req.repeat > 0 and i + 1 >= req.repeat:
                break
            if "transmit" in active_processes:
                await asyncio.sleep(0.5)
        active_processes.pop("transmit", None)
        _try_unlink(wav_file)

    sentinel = await asyncio.create_subprocess_exec("true")
    active_processes["transmit"] = sentinel
    asyncio.create_task(run_tts())

    return {
        "status": "transmitting",
        "modulation": req.modulation,
        "message": req.message,
        "frequency_mhz": req.frequency,
    }


# ── Log endpoints ────────────────────────────────────────────────────────────

@app.get("/api/logs")
async def query_logs(
    category: str = Query("_", description="Category filter"),
    severity: str = Query("_", description="Severity filter"),
    search: str = Query("_", description="Search text"),
    limit: int = Query(50, description="Max results"),
):
    """Query event logs."""
    # Sanitize inputs
    if category not in VALID_LOG_CATEGORIES:
        category = "_"
    if severity not in VALID_LOG_SEVERITIES:
        severity = "_"
    limit = max(1, min(limit, 500))
    # Prevent shell metacharacters in search — passed as subprocess arg, not shell
    search_safe = search if search else "_"

    proc = await asyncio.create_subprocess_exec(
        "python3", str(TRANSMIT_PY),
        "LOGSTORE_QUERY", category, severity, search_safe, str(limit),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return {"output": stdout.decode(errors="replace"), "error": stderr.decode(errors="replace")}


@app.get("/api/logs/stats")
async def log_stats():
    """Log statistics."""
    proc = await asyncio.create_subprocess_exec(
        "python3", str(TRANSMIT_PY), "LOGSTORE_STATS",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return {"output": stdout.decode(errors="replace")}


@app.post("/api/logs/export")
async def export_logs(req: ExportRequest):
    """Export logs."""
    export_dir = SCRIPT_DIR / "hackrf_logs"
    export_dir.mkdir(exist_ok=True)
    ext = {"text": "txt", "json": "json", "csv": "csv"}.get(req.format, "txt")
    export_file = export_dir / f"export_{int(time.time())}.{ext}"

    proc = await asyncio.create_subprocess_exec(
        "python3", str(TRANSMIT_PY),
        "LOGSTORE_EXPORT", req.format, str(export_file),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if export_file.exists():
        content = export_file.read_text(errors="replace")
        return {"file": str(export_file), "content": content}
    return {"output": stdout.decode(errors="replace"), "error": stderr.decode(errors="replace")}


@app.post("/api/logs/clear")
async def clear_logs(req: ClearRequest):
    """Archive and clear logs."""
    args = ["python3", str(TRANSMIT_PY), "LOGSTORE_CLEAR"]
    if req.no_archive:
        args.append("no_archive")
    proc = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return {"output": stdout.decode(errors="replace")}


# ── WebSocket Endpoints ──────────────────────────────────────────────────────

def _validate_ws_config(config: dict, fields: dict) -> dict:
    """Validate and clamp WebSocket config values."""
    result = {}
    for key, (default, validator) in fields.items():
        val = config.get(key, default)
        result[key] = validator(val) if validator else val
    return result


def _clamp_int(lo, hi):
    def _clamp(v):
        return max(lo, min(hi, int(v)))
    return _clamp


def _clamp_float(lo, hi):
    def _clamp(v):
        return max(lo, min(hi, float(v)))
    return _clamp


def _whitelist(valid_set, default):
    def _check(v):
        return v if v in valid_set else default
    return _check


@app.websocket("/ws/analyzer")
async def ws_analyzer(ws: WebSocket):
    """Signal Analyzer loop."""
    await ws.accept()
    try:
        raw_config = await ws.receive_json()
        c = _validate_ws_config(raw_config, {
            "demod":      ("DEMOD_NBFM", _whitelist(VALID_DEMOD_MODES, "DEMOD_NBFM")),
            "decode":     ("DECODE_AUTO", _whitelist(VALID_DECODE_MODES, "DECODE_AUTO")),
            "frequency":  (462.7, _clamp_float(0.1, 7250)),
            "listen_sec": (10, _clamp_int(1, 120)),
            "lna_gain":   (16, _clamp_int(0, 40)),
            "vga_gain":   (20, _clamp_int(0, 62)),
        })

        freq_hz = int(c["frequency"] * 1_000_000)
        num_samples = int(SAMPLE_RATE * c["listen_sec"])
        ws_key = "analyzer"
        round_num = 1

        while True:
            await ws.send_json({"type": "status", "round": round_num, "state": "listening"})

            rx_file = _mktemp(suffix=".raw", prefix="hackrf_sa_rx_")
            proc = await asyncio.create_subprocess_exec(
                "hackrf_transfer", "-r", rx_file,
                "-f", str(freq_hz), "-s", str(SAMPLE_RATE),
                "-l", str(c["lna_gain"]), "-g", str(c["vga_gain"]),
                "-n", str(num_samples),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            active_processes[ws_key] = proc
            await proc.wait()

            if not os.path.isfile(rx_file) or os.path.getsize(rx_file) == 0:
                await ws.send_json({"type": "status", "round": round_num, "state": "no_data"})
                _try_unlink(rx_file)
                round_num += 1
                await asyncio.sleep(1)
                continue

            # Demodulate
            await ws.send_json({"type": "status", "round": round_num, "state": "demodulating"})
            demod_wav = _mktemp(suffix=".wav", prefix="hackrf_sa_demod_")
            proc = await asyncio.create_subprocess_exec(
                "python3", str(TRANSMIT_PY), c["demod"], rx_file, demod_wav,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.wait()
            _try_unlink(rx_file)

            if not os.path.isfile(demod_wav) or os.path.getsize(demod_wav) == 0:
                await ws.send_json({"type": "status", "round": round_num, "state": "demod_failed"})
                _try_unlink(demod_wav)
                round_num += 1
                await asyncio.sleep(1)
                continue

            # Decode
            await ws.send_json({"type": "status", "round": round_num, "state": "decoding"})
            proc = await asyncio.create_subprocess_exec(
                "python3", str(TRANSMIT_PY), c["decode"], demod_wav,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            _try_unlink(demod_wav)

            decoded = stdout.decode(errors="replace").strip()
            await ws.send_json({
                "type": "result",
                "round": round_num,
                "decoded": decoded,
                "error": stderr.decode(errors="replace").strip(),
            })

            round_num += 1
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        await kill_process("analyzer")
    except asyncio.CancelledError:
        await kill_process("analyzer")
    except Exception as e:
        try:
            await ws.send_json({"type": "error", "message": str(e)})
            await ws.close(1011)
        except Exception:
            pass
        await kill_process("analyzer")


@app.websocket("/ws/jitter")
async def ws_jitter(ws: WebSocket):
    """Jitter Analysis loop."""
    await ws.accept()
    try:
        raw_config = await ws.receive_json()
        c = _validate_ws_config(raw_config, {
            "demod":       ("DEMOD_NBFM", _whitelist(VALID_DEMOD_MODES, "DEMOD_NBFM")),
            "demod_label": ("NBFM", lambda v: str(v)[:10]),
            "frequency":   (462.7, _clamp_float(0.1, 7250)),
            "listen_sec":  (13.7, _clamp_float(0.1, 120)),
            "lna_gain":    (16, _clamp_int(0, 40)),
            "vga_gain":    (20, _clamp_int(0, 62)),
        })

        freq_hz = int(c["frequency"] * 1_000_000)
        num_samples = int(SAMPLE_RATE * c["listen_sec"])
        ws_key = "jitter"

        # Start logging session
        sess_proc = await asyncio.create_subprocess_exec(
            "python3", str(TRANSMIT_PY),
            "LOGSTORE_SESSION_START", str(c["frequency"]),
            c["demod_label"], "Jitter frequency data",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        sess_stdout, _ = await sess_proc.communicate()
        session_id = sess_stdout.decode(errors="replace").strip()
        await ws.send_json({"type": "session", "session_id": session_id})

        round_num = 1
        while True:
            await ws.send_json({"type": "status", "round": round_num, "state": "listening"})

            rx_file = _mktemp(suffix=".raw", prefix="hackrf_jf_rx_")
            proc = await asyncio.create_subprocess_exec(
                "hackrf_transfer", "-r", rx_file,
                "-f", str(freq_hz), "-s", str(SAMPLE_RATE),
                "-l", str(c["lna_gain"]), "-g", str(c["vga_gain"]),
                "-n", str(num_samples),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            active_processes[ws_key] = proc
            await proc.wait()

            if not os.path.isfile(rx_file) or os.path.getsize(rx_file) == 0:
                await ws.send_json({"type": "status", "round": round_num, "state": "no_data"})
                _try_unlink(rx_file)
                round_num += 1
                await asyncio.sleep(1)
                continue

            # Demodulate
            await ws.send_json({"type": "status", "round": round_num, "state": "demodulating"})
            demod_wav = _mktemp(suffix=".wav", prefix="hackrf_jf_demod_")
            proc = await asyncio.create_subprocess_exec(
                "python3", str(TRANSMIT_PY), c["demod"], rx_file, demod_wav,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.wait()
            _try_unlink(rx_file)

            if not os.path.isfile(demod_wav) or os.path.getsize(demod_wav) == 0:
                await ws.send_json({"type": "status", "round": round_num, "state": "demod_failed"})
                _try_unlink(demod_wav)
                round_num += 1
                await asyncio.sleep(1)
                continue

            # Jitter analysis
            await ws.send_json({"type": "status", "round": round_num, "state": "analyzing"})
            proc = await asyncio.create_subprocess_exec(
                "python3", str(TRANSMIT_PY),
                "JITTER_ANALYZE", demod_wav,
                str(c["frequency"]), c["demod_label"],
                str(c["listen_sec"]), session_id,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            _try_unlink(demod_wav)

            await ws.send_json({
                "type": "result",
                "round": round_num,
                "output": stdout.decode(errors="replace"),
                "error": stderr.decode(errors="replace").strip(),
            })

            round_num += 1
            await asyncio.sleep(2)

    except WebSocketDisconnect:
        await kill_process("jitter")
    except asyncio.CancelledError:
        await kill_process("jitter")
    except Exception as e:
        try:
            await ws.send_json({"type": "error", "message": str(e)})
            await ws.close(1011)
        except Exception:
            pass
        await kill_process("jitter")


@app.websocket("/ws/ai")
async def ws_ai(ws: WebSocket):
    """AI Voice Responder loop."""
    await ws.accept()
    try:
        raw_config = await ws.receive_json()
        c = _validate_ws_config(raw_config, {
            "demod":         ("DEMOD_NBFM", _whitelist(VALID_DEMOD_MODES, "DEMOD_NBFM")),
            "tx_mode":       ("WAV_NBFM", _whitelist(VALID_WAV_MODES, "WAV_NBFM")),
            "frequency":     (462.7, _clamp_float(0.1, 7250)),
            "listen_sec":    (5, _clamp_int(1, 60)),
            "lna_gain":      (16, _clamp_int(0, 40)),
            "vga_gain":      (20, _clamp_int(0, 62)),
            "tx_gain":       (47, _clamp_int(0, 47)),
            "tts_voice":     ("en", _whitelist(VALID_VOICES, "en")),
            "tts_speed":     (150, _clamp_int(50, 400)),
            "whisper_model": ("base.en", _whitelist(VALID_WHISPER_MODELS, "base.en")),
        })

        freq_hz = int(c["frequency"] * 1_000_000)
        num_samples = int(SAMPLE_RATE * c["listen_sec"])
        ws_key = "ai"

        whisper_bin = SCRIPT_DIR / "whisper.cpp" / "main"
        whisper_model_path = SCRIPT_DIR / "whisper.cpp" / "models" / f"ggml-{c['whisper_model']}.bin"
        llama_bin = SCRIPT_DIR / "llama.cpp" / "llama-cli"
        if not llama_bin.exists():
            llama_bin = SCRIPT_DIR / "llama.cpp" / "main"
        llama_model = SCRIPT_DIR / "llama.cpp" / "models" / "qwen2.5-1.5b-instruct-q4_k_m.gguf"

        # Validate AI dependencies before entering loop
        if not whisper_bin.exists():
            await ws.send_json({"type": "error", "message": f"whisper.cpp not found at {whisper_bin}. Run install.sh --full"})
            return
        if not whisper_model_path.exists():
            await ws.send_json({"type": "error", "message": f"Whisper model not found: {whisper_model_path}. Run install.sh --full"})
            return
        if not llama_bin.exists():
            await ws.send_json({"type": "error", "message": "llama.cpp not found. Run install.sh --full"})
            return
        if not llama_model.exists():
            await ws.send_json({"type": "error", "message": f"LLM model not found: {llama_model}. Run install.sh --full"})
            return

        round_num = 1
        while True:
            await ws.send_json({"type": "status", "round": round_num, "state": "listening"})

            # 1. Capture IQ
            rx_file = _mktemp(suffix=".raw", prefix="hackrf_ai_rx_")
            proc = await asyncio.create_subprocess_exec(
                "hackrf_transfer", "-r", rx_file,
                "-f", str(freq_hz), "-s", str(SAMPLE_RATE),
                "-l", str(c["lna_gain"]), "-g", str(c["vga_gain"]),
                "-n", str(num_samples),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            active_processes[ws_key] = proc
            await proc.wait()

            if not os.path.isfile(rx_file) or os.path.getsize(rx_file) == 0:
                await ws.send_json({"type": "status", "round": round_num, "state": "no_data"})
                _try_unlink(rx_file)
                round_num += 1
                await asyncio.sleep(1)
                continue

            # 2. Demodulate
            await ws.send_json({"type": "status", "round": round_num, "state": "demodulating"})
            demod_wav = _mktemp(suffix=".wav", prefix="hackrf_ai_demod_")
            proc = await asyncio.create_subprocess_exec(
                "python3", str(TRANSMIT_PY), c["demod"], rx_file, demod_wav,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.wait()
            _try_unlink(rx_file)

            if not os.path.isfile(demod_wav) or os.path.getsize(demod_wav) == 0:
                await ws.send_json({"type": "status", "round": round_num, "state": "demod_failed"})
                _try_unlink(demod_wav)
                round_num += 1
                await asyncio.sleep(1)
                continue

            # 3. Transcribe
            await ws.send_json({"type": "status", "round": round_num, "state": "transcribing"})
            proc = await asyncio.create_subprocess_exec(
                str(whisper_bin), "-m", str(whisper_model_path),
                "-f", demod_wav, "--no-prints", "--no-timestamps", "-l", "en",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            _try_unlink(demod_wav)
            transcript = " ".join(stdout.decode(errors="replace").split()).strip()

            if not transcript:
                await ws.send_json({"type": "status", "round": round_num, "state": "no_speech"})
                round_num += 1
                await asyncio.sleep(1)
                continue

            await ws.send_json({"type": "transcript", "round": round_num, "text": transcript})

            # 4. LLM response
            await ws.send_json({"type": "status", "round": round_num, "state": "thinking"})
            prompt = (
                "<|im_start|>system\n"
                "You are a helpful AI radio assistant. Keep responses concise, clear, "
                "and conversational. They will be spoken aloud via text-to-speech over radio. "
                "Limit to 2-3 sentences. Avoid special characters, URLs, and code.<|im_end|>\n"
                f"<|im_start|>user\n{transcript}<|im_end|>\n"
                "<|im_start|>assistant\n"
            )
            proc = await asyncio.create_subprocess_exec(
                str(llama_bin), "-m", str(llama_model),
                "-p", prompt, "-n", "200", "-c", "512",
                "--temp", "0.7", "--no-display-prompt", "-e", "--no-perf",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await proc.communicate()
            ai_text = stdout.decode(errors="replace")
            for marker in ["<|im_end|>", "[end of text]"]:
                if marker in ai_text:
                    ai_text = ai_text[:ai_text.index(marker)]
            ai_text = " ".join(ai_text.split()).strip()

            if not ai_text:
                await ws.send_json({"type": "status", "round": round_num, "state": "no_response"})
                round_num += 1
                await asyncio.sleep(1)
                continue

            await ws.send_json({"type": "response", "round": round_num, "text": ai_text})

            # 5. TTS
            await ws.send_json({"type": "status", "round": round_num, "state": "speaking"})
            tts_wav = _mktemp(suffix=".wav", prefix="hackrf_ai_tts_")
            proc = await asyncio.create_subprocess_exec(
                "espeak-ng", "-v", c["tts_voice"], "-s", str(c["tts_speed"]),
                "-w", tts_wav, ai_text,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            await proc.wait()

            if not os.path.isfile(tts_wav) or os.path.getsize(tts_wav) == 0:
                await ws.send_json({"type": "status", "round": round_num, "state": "tts_failed"})
                _try_unlink(tts_wav)
                round_num += 1
                await asyncio.sleep(1)
                continue

            # 6. Transmit
            await ws.send_json({"type": "status", "round": round_num, "state": "transmitting"})
            tx_cmd = _build_wav_tx_pipeline(
                c["tx_mode"], tts_wav, freq_hz, c["tx_gain"],
            )
            proc = await asyncio.create_subprocess_exec(
                "bash", "-c", tx_cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            active_processes[ws_key] = proc
            await proc.wait()
            _try_unlink(tts_wav)

            await ws.send_json({"type": "status", "round": round_num, "state": "done"})
            round_num += 1
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        await kill_process("ai")
    except asyncio.CancelledError:
        await kill_process("ai")
    except Exception as e:
        try:
            await ws.send_json({"type": "error", "message": str(e)})
            await ws.close(1011)
        except Exception:
            pass
        await kill_process("ai")


@app.websocket("/ws/record")
async def ws_record(ws: WebSocket):
    """Record & Retransmit."""
    await ws.accept()
    rec_file = None
    try:
        raw_config = await ws.receive_json()
        c = _validate_ws_config(raw_config, {
            "rx_frequency": (462.7, _clamp_float(0.1, 7250)),
            "tx_frequency": (462.7, _clamp_float(0.1, 7250)),
            "lna_gain":     (16, _clamp_int(0, 40)),
            "vga_gain":     (20, _clamp_int(0, 62)),
            "tx_gain":      (47, _clamp_int(0, 47)),
            "duration":     (5, _clamp_int(1, 300)),
            "repeat":       (1, _clamp_int(0, 9999)),
        })

        rx_freq_hz = int(c["rx_frequency"] * 1_000_000)
        tx_freq_hz = int(c["tx_frequency"] * 1_000_000)
        num_samples = int(SAMPLE_RATE * c["duration"])
        ws_key = "record"

        # Record
        await ws.send_json({"type": "status", "state": "recording", "duration": c["duration"]})
        rec_file = _mktemp(suffix=".raw", prefix="hackrf_rec_")
        proc = await asyncio.create_subprocess_exec(
            "hackrf_transfer", "-r", rec_file,
            "-f", str(rx_freq_hz), "-s", str(SAMPLE_RATE),
            "-l", str(c["lna_gain"]), "-g", str(c["vga_gain"]),
            "-n", str(num_samples),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        active_processes[ws_key] = proc
        await proc.wait()

        if not os.path.isfile(rec_file) or os.path.getsize(rec_file) == 0:
            await ws.send_json({"type": "error", "message": "No data recorded"})
            _try_unlink(rec_file)
            rec_file = None
            return

        file_size = os.path.getsize(rec_file)
        cap_duration = file_size / (SAMPLE_RATE * 2)
        await ws.send_json({
            "type": "status", "state": "ready",
            "file_size": file_size,
            "duration": round(cap_duration, 2),
        })

        # Wait for retransmit command
        cmd = await ws.receive_json()
        if cmd.get("action") != "retransmit":
            _try_unlink(rec_file)
            rec_file = None
            return

        # Retransmit
        iterations = c["repeat"] if c["repeat"] > 0 else 999_999
        for i in range(iterations):
            await ws.send_json({"type": "status", "state": "transmitting", "iteration": i + 1})
            proc = await asyncio.create_subprocess_exec(
                "hackrf_transfer", "-t", rec_file,
                "-f", str(tx_freq_hz), "-s", str(SAMPLE_RATE),
                "-x", str(c["tx_gain"]), "-a", "1",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            active_processes[ws_key] = proc
            await proc.wait()
            if c["repeat"] > 0 and i + 1 >= c["repeat"]:
                break
            await asyncio.sleep(0.5)

        await ws.send_json({"type": "status", "state": "complete"})
        _try_unlink(rec_file)
        rec_file = None

    except WebSocketDisconnect:
        await kill_process("record")
        if rec_file:
            _try_unlink(rec_file)
    except asyncio.CancelledError:
        await kill_process("record")
        if rec_file:
            _try_unlink(rec_file)
    except Exception as e:
        try:
            await ws.send_json({"type": "error", "message": str(e)})
            await ws.close(1011)
        except Exception:
            pass
        await kill_process("record")
        if rec_file:
            _try_unlink(rec_file)


def _try_unlink(path: str):
    try:
        os.unlink(path)
    except OSError:
        pass


def _mktemp(suffix: str = "", prefix: str = "tmp") -> str:
    """Create a temp file securely and return its path (closed immediately)."""
    fd, path = tempfile.mkstemp(suffix=suffix, prefix=prefix)
    os.close(fd)
    return path


# ── Static files + SPA fallback ─────────────────────────────────────────────
static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
