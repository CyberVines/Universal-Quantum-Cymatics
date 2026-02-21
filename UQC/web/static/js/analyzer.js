/* ═══════════════════════════════════════════════════════════════════════════
   Signal Analyzer / Decoder
   ═══════════════════════════════════════════════════════════════════════════ */
import { WS, toast, log, updateStatusBar, bindRange } from './app.js';

let ws = null;
let running = false;

const DEMOD_OPTIONS = [
    { value: 'DEMOD_NBFM', label: 'NBFM' },
    { value: 'DEMOD_WBFM', label: 'WBFM' },
    { value: 'DEMOD_AM', label: 'AM' },
    { value: 'DEMOD_USB', label: 'USB' },
    { value: 'DEMOD_LSB', label: 'LSB' },
];

const DECODE_OPTIONS = [
    { value: 'DECODE_AUTO', label: 'Auto-detect' },
    { value: 'DECODE_CW', label: 'CW / Morse' },
    { value: 'DECODE_RTTY', label: 'RTTY' },
    { value: 'DECODE_BPSK31', label: 'BPSK31' },
    { value: 'DECODE_BPSK63', label: 'BPSK63' },
    { value: 'DECODE_BPSK125', label: 'BPSK125' },
    { value: 'DECODE_AFSK1200', label: 'AFSK1200 (AX.25/APRS)' },
    { value: 'DECODE_MFSK16', label: 'MFSK16' },
    { value: 'DECODE_MFSK32', label: 'MFSK32' },
    { value: 'DECODE_MFSK64', label: 'MFSK64' },
    { value: 'DECODE_OLIVIA8', label: 'Olivia 8/500' },
    { value: 'DECODE_OLIVIA16', label: 'Olivia 16/500' },
    { value: 'DECODE_OLIVIA32', label: 'Olivia 32/1000' },
    { value: 'DECODE_FT8', label: 'FT8' },
    { value: 'DECODE_MUSIC_CIPHER', label: 'Musical Cipher' },
];

export function initAnalyzer() {
    const container = document.getElementById('view-analyzer');

    const demodOpts = DEMOD_OPTIONS.map(o => `<option value="${o.value}">${o.label}</option>`).join('');
    const decodeOpts = DECODE_OPTIONS.map(o => `<option value="${o.value}">${o.label}</option>`).join('');

    container.innerHTML = `
        <h2 class="section-title">Signal Analyzer / Decoder</h2>
        <p class="section-subtitle">Receive, demodulate, and decode signals in a continuous loop.</p>

        <div class="form-row">
            <div class="form-group">
                <label>Frequency (MHz)</label>
                <input type="number" id="sa-freq" value="462.700" step="0.001">
            </div>
            <div class="form-group">
                <label>Demod Mode</label>
                <select id="sa-demod">${demodOpts}</select>
            </div>
            <div class="form-group">
                <label>Decode Mode</label>
                <select id="sa-decode">${decodeOpts}</select>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Listen Duration (sec)</label>
                <div class="range-row">
                    <input type="range" id="sa-listen" min="2" max="60" value="10">
                    <span class="range-value" id="sa-listen-val">10</span>
                </div>
            </div>
            <div class="form-group">
                <label>LNA Gain</label>
                <div class="range-row">
                    <input type="range" id="sa-lna" min="0" max="40" step="8" value="16">
                    <span class="range-value" id="sa-lna-val">16</span>
                </div>
            </div>
            <div class="form-group">
                <label>VGA Gain</label>
                <div class="range-row">
                    <input type="range" id="sa-vga" min="0" max="62" step="2" value="20">
                    <span class="range-value" id="sa-vga-val">20</span>
                </div>
            </div>
        </div>

        <div class="btn-group">
            <button class="btn btn-primary btn-large" id="btn-sa-start">START</button>
            <button class="btn btn-danger btn-large" id="btn-sa-stop" style="display:none">STOP</button>
        </div>

        <label style="margin-top:16px">Decoded Output</label>
        <div class="terminal" id="sa-terminal" style="margin-top:8px;min-height:200px"></div>
    `;

    bindRange('sa-listen', 'sa-listen-val');
    bindRange('sa-lna', 'sa-lna-val');
    bindRange('sa-vga', 'sa-vga-val');

    document.getElementById('btn-sa-start').addEventListener('click', start);
    document.getElementById('btn-sa-stop').addEventListener('click', stop);
}

function start() {
    if (running) return;
    running = true;

    const freq = parseFloat(document.getElementById('sa-freq').value);
    const terminal = document.getElementById('sa-terminal');
    terminal.textContent = '';

    document.getElementById('btn-sa-start').style.display = 'none';
    document.getElementById('btn-sa-stop').style.display = '';

    updateStatusBar(freq, 'Analyzer');
    log(`Signal Analyzer started on ${freq} MHz`, 'info');

    ws = new WS('/ws/analyzer');

    ws.on('status', (data) => {
        const labels = {
            listening: 'Listening...',
            demodulating: 'Demodulating...',
            decoding: 'Decoding...',
            no_data: 'No data captured',
            demod_failed: 'Demodulation failed',
        };
        appendLine(terminal, `[Round ${data.round}] ${labels[data.state] || data.state}`, 'line-dim');
    });

    ws.on('result', (data) => {
        if (data.decoded) {
            appendLine(terminal, `── Round ${data.round} Result ──`, 'line-cyan');
            data.decoded.split('\n').forEach(line => {
                appendLine(terminal, line, 'line-green');
            });
        } else {
            appendLine(terminal, `[Round ${data.round}] (no signal decoded)`, 'line-dim');
        }
        appendLine(terminal, '');
    });

    ws.on('error', (data) => {
        appendLine(terminal, `ERROR: ${data.message}`, 'line-red');
        toast(data.message || 'Analyzer error', 'error');
        cleanup();
    });

    ws.on('close', () => cleanup());

    ws.connect({
        demod: document.getElementById('sa-demod').value,
        decode: document.getElementById('sa-decode').value,
        frequency: freq,
        listen_sec: parseInt(document.getElementById('sa-listen').value),
        lna_gain: parseInt(document.getElementById('sa-lna').value),
        vga_gain: parseInt(document.getElementById('sa-vga').value),
    });
}

function stop() {
    if (ws) ws.close();
    cleanup();
    log('Signal Analyzer stopped', 'warn');
    toast('Analyzer stopped', 'warning');
}

function cleanup() {
    if (!running) return;
    running = false;
    ws = null;
    document.getElementById('btn-sa-start').style.display = '';
    document.getElementById('btn-sa-stop').style.display = 'none';
    updateStatusBar(undefined, '--');
}

function appendLine(el, text, cls = '') {
    const line = document.createElement('div');
    line.className = `line ${cls}`;
    line.textContent = text;
    el.appendChild(line);
    el.scrollTop = el.scrollHeight;
}
