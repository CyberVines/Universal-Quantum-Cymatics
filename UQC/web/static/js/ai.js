/* ═══════════════════════════════════════════════════════════════════════════
   AI Voice Responder — Listen → Transcribe → LLM → TTS → Transmit
   ═══════════════════════════════════════════════════════════════════════════ */
import { WS, toast, log, updateStatusBar, bindRange } from './app.js';

let ws = null;
let running = false;

const DEMOD_MAP = {
    NBFM: { demod: 'DEMOD_NBFM', tx: 'WAV_NBFM' },
    WBFM: { demod: 'DEMOD_WBFM', tx: 'WAV_WBFM' },
    AM:   { demod: 'DEMOD_AM',   tx: 'WAV_AM' },
    USB:  { demod: 'DEMOD_USB',  tx: 'WAV_USB' },
    LSB:  { demod: 'DEMOD_LSB',  tx: 'WAV_LSB' },
};

export function initAI() {
    const container = document.getElementById('view-ai');

    container.innerHTML = `
        <h2 class="section-title">AI Voice Responder</h2>
        <p class="section-subtitle">Listen on frequency, transcribe with Whisper, respond via local LLM, speak back over radio.</p>

        <div class="form-row">
            <div class="form-group">
                <label>Frequency (MHz)</label>
                <input type="number" id="ai-freq" value="462.700" step="0.001">
            </div>
            <div class="form-group">
                <label>Modulation</label>
                <select id="ai-mod">
                    <option value="NBFM">NBFM</option>
                    <option value="WBFM">WBFM</option>
                    <option value="AM">AM</option>
                    <option value="USB">USB</option>
                    <option value="LSB">LSB</option>
                </select>
            </div>
            <div class="form-group">
                <label>Listen Duration (sec)</label>
                <div class="range-row">
                    <input type="range" id="ai-listen" min="2" max="30" value="5">
                    <span class="range-value" id="ai-listen-val">5</span>
                </div>
            </div>
        </div>

        <div class="param-panel">
            <div class="panel-title">RF / Voice Settings</div>
            <div class="form-row">
                <div class="form-group">
                    <label>LNA Gain</label>
                    <div class="range-row">
                        <input type="range" id="ai-lna" min="0" max="40" step="8" value="16">
                        <span class="range-value" id="ai-lna-val">16</span>
                    </div>
                </div>
                <div class="form-group">
                    <label>VGA Gain</label>
                    <div class="range-row">
                        <input type="range" id="ai-vga" min="0" max="62" step="2" value="20">
                        <span class="range-value" id="ai-vga-val">20</span>
                    </div>
                </div>
                <div class="form-group">
                    <label>TX Gain</label>
                    <div class="range-row">
                        <input type="range" id="ai-tx-gain" min="0" max="47" value="47">
                        <span class="range-value" id="ai-tx-gain-val">47</span>
                    </div>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>TTS Voice</label>
                    <select id="ai-voice">
                        <option value="en">English</option>
                        <option value="en-us">English (US)</option>
                        <option value="en-gb">English (GB)</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>TTS Speed (WPM)</label>
                    <div class="range-row">
                        <input type="range" id="ai-tts-speed" min="50" max="300" value="150">
                        <span class="range-value" id="ai-tts-speed-val">150</span>
                    </div>
                </div>
                <div class="form-group">
                    <label>Whisper Model</label>
                    <select id="ai-whisper">
                        <option value="tiny.en">tiny.en</option>
                        <option value="base.en" selected>base.en</option>
                        <option value="small.en">small.en</option>
                        <option value="medium.en">medium.en</option>
                    </select>
                </div>
            </div>
        </div>

        <div class="btn-group">
            <button class="btn btn-primary btn-large" id="btn-ai-start">START</button>
            <button class="btn btn-danger btn-large" id="btn-ai-stop" style="display:none">STOP</button>
        </div>

        <div class="ai-panel" style="margin-top:20px">
            <div class="ai-live">
                <div class="live-label">Round</div>
                <div class="live-text" id="ai-round">--</div>
                <div class="live-status" id="ai-state">Idle</div>
            </div>
            <div class="ai-live">
                <div class="live-label">Last Transcript</div>
                <div class="live-text" id="ai-transcript">--</div>
            </div>
            <div class="ai-live" style="grid-column:1/-1">
                <div class="live-label">AI Response</div>
                <div class="live-text" id="ai-response">--</div>
            </div>
        </div>

        <label style="margin-top:16px">Session Log</label>
        <div class="terminal" id="ai-terminal" style="margin-top:8px;min-height:120px"></div>
    `;

    bindRange('ai-listen', 'ai-listen-val');
    bindRange('ai-lna', 'ai-lna-val');
    bindRange('ai-vga', 'ai-vga-val');
    bindRange('ai-tx-gain', 'ai-tx-gain-val');
    bindRange('ai-tts-speed', 'ai-tts-speed-val');

    document.getElementById('btn-ai-start').addEventListener('click', start);
    document.getElementById('btn-ai-stop').addEventListener('click', stop);
}

const STATE_LABELS = {
    listening: 'Listening...',
    demodulating: 'Demodulating...',
    transcribing: 'Transcribing (Whisper)...',
    thinking: 'Generating response (LLM)...',
    speaking: 'Generating TTS...',
    transmitting: 'Transmitting response...',
    done: 'Round complete',
    no_data: 'No data captured',
    demod_failed: 'Demodulation failed',
    no_speech: 'No speech detected',
    no_response: 'LLM produced no response',
    tts_failed: 'TTS generation failed',
};

function start() {
    if (running) return;
    running = true;

    const freq = parseFloat(document.getElementById('ai-freq').value);
    const modKey = document.getElementById('ai-mod').value;
    const mod = DEMOD_MAP[modKey];

    document.getElementById('btn-ai-start').style.display = 'none';
    document.getElementById('btn-ai-stop').style.display = '';
    document.getElementById('ai-terminal').textContent = '';

    updateStatusBar(freq, `AI ${modKey}`);
    log(`AI Responder started on ${freq} MHz (${modKey})`, 'info');

    ws = new WS('/ws/ai');

    ws.on('status', (data) => {
        document.getElementById('ai-round').textContent = `#${data.round}`;
        document.getElementById('ai-state').textContent = STATE_LABELS[data.state] || data.state;
        appendLine(`[Round ${data.round}] ${STATE_LABELS[data.state] || data.state}`);
    });

    ws.on('transcript', (data) => {
        document.getElementById('ai-transcript').textContent = data.text;
        appendLine(`  Heard: ${data.text}`, 'line-cyan');
    });

    ws.on('response', (data) => {
        document.getElementById('ai-response').textContent = data.text;
        appendLine(`  AI: ${data.text}`, 'line-green');
    });

    ws.on('error', (data) => {
        appendLine(`ERROR: ${data.message}`, 'line-red');
        toast(data.message || 'AI Responder error', 'error');
        cleanup();
    });

    ws.on('close', () => cleanup());

    ws.connect({
        demod: mod.demod,
        tx_mode: mod.tx,
        frequency: freq,
        listen_sec: parseInt(document.getElementById('ai-listen').value),
        lna_gain: parseInt(document.getElementById('ai-lna').value),
        vga_gain: parseInt(document.getElementById('ai-vga').value),
        tx_gain: parseInt(document.getElementById('ai-tx-gain').value),
        tts_voice: document.getElementById('ai-voice').value,
        tts_speed: parseInt(document.getElementById('ai-tts-speed').value),
        whisper_model: document.getElementById('ai-whisper').value,
    });
}

function stop() {
    if (ws) ws.close();
    cleanup();
    log('AI Responder stopped', 'warn');
    toast('AI Responder stopped', 'warning');
}

function cleanup() {
    if (!running) return;
    running = false;
    ws = null;
    document.getElementById('btn-ai-start').style.display = '';
    document.getElementById('btn-ai-stop').style.display = 'none';
    document.getElementById('ai-state').textContent = 'Idle';
    updateStatusBar(undefined, '--');
}

function appendLine(text, cls = '') {
    const terminal = document.getElementById('ai-terminal');
    const line = document.createElement('div');
    line.className = `line ${cls}`;
    line.textContent = text;
    terminal.appendChild(line);
    terminal.scrollTop = terminal.scrollHeight;
}
