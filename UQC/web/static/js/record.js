/* ═══════════════════════════════════════════════════════════════════════════
   Record & Retransmit
   ═══════════════════════════════════════════════════════════════════════════ */
import { WS, toast, log, updateStatusBar, bindRange, formatBytes } from './app.js';

let ws = null;
let running = false;

export function initRecord() {
    const container = document.getElementById('view-record');

    container.innerHTML = `
        <h2 class="section-title">Record &amp; Retransmit</h2>
        <p class="section-subtitle">Capture IQ from HackRF on one frequency, then retransmit on another.</p>

        <div class="form-row">
            <div class="form-group">
                <label>RX Frequency (MHz)</label>
                <input type="number" id="rec-rx-freq" value="462.700" step="0.001">
            </div>
            <div class="form-group">
                <label>TX Frequency (MHz)</label>
                <input type="number" id="rec-tx-freq" value="462.700" step="0.001">
            </div>
        </div>

        <div class="param-panel">
            <div class="panel-title">RF Receive Gain</div>
            <div class="form-row">
                <div class="form-group">
                    <label>LNA Gain (0-40, step 8)</label>
                    <div class="range-row">
                        <input type="range" id="rec-lna" min="0" max="40" step="8" value="16">
                        <span class="range-value" id="rec-lna-val">16</span>
                    </div>
                </div>
                <div class="form-group">
                    <label>VGA Gain (0-62, step 2)</label>
                    <div class="range-row">
                        <input type="range" id="rec-vga" min="0" max="62" step="2" value="20">
                        <span class="range-value" id="rec-vga-val">20</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Record Duration (seconds)</label>
                <input type="number" id="rec-duration" value="5" min="1" max="300">
            </div>
            <div class="form-group">
                <label>TX Gain (dB)</label>
                <div class="range-row">
                    <input type="range" id="rec-tx-gain" min="0" max="47" value="47">
                    <span class="range-value" id="rec-tx-gain-val">47</span>
                </div>
            </div>
            <div class="form-group">
                <label>Repeat</label>
                <div class="repeat-control">
                    <input type="number" id="rec-repeat" value="1" min="0" max="9999">
                    <span class="repeat-label">0 = continuous</span>
                </div>
            </div>
        </div>

        <div class="btn-group">
            <button class="btn btn-primary btn-large" id="btn-rec-start">RECORD</button>
            <button class="btn btn-cyan" id="btn-rec-retransmit" style="display:none">RETRANSMIT</button>
            <button class="btn btn-danger" id="btn-rec-stop" style="display:none">STOP</button>
        </div>

        <div class="terminal" id="rec-terminal" style="margin-top:16px;min-height:80px"></div>
    `;

    bindRange('rec-lna', 'rec-lna-val');
    bindRange('rec-vga', 'rec-vga-val');
    bindRange('rec-tx-gain', 'rec-tx-gain-val');

    document.getElementById('btn-rec-start').addEventListener('click', startRecord);
    document.getElementById('btn-rec-retransmit').addEventListener('click', retransmit);
    document.getElementById('btn-rec-stop').addEventListener('click', stopRecord);
}

function startRecord() {
    if (running) return;
    running = true;

    const rxFreq = parseFloat(document.getElementById('rec-rx-freq').value);
    const txFreq = parseFloat(document.getElementById('rec-tx-freq').value);
    const lna = parseInt(document.getElementById('rec-lna').value);
    const vga = parseInt(document.getElementById('rec-vga').value);
    const txGain = parseInt(document.getElementById('rec-tx-gain').value);
    const duration = parseInt(document.getElementById('rec-duration').value);
    const repeat = parseInt(document.getElementById('rec-repeat').value) || 1;

    const terminal = document.getElementById('rec-terminal');
    terminal.textContent = '';

    updateStatusBar(rxFreq, 'Recording');
    appendLine(terminal, `Recording on ${rxFreq} MHz for ${duration}s...`);

    document.getElementById('btn-rec-start').style.display = 'none';
    document.getElementById('btn-rec-stop').style.display = '';

    ws = new WS('/ws/record');
    ws.on('status', (data) => {
        if (data.state === 'recording') {
            appendLine(terminal, `Recording ${data.duration}s...`, 'line-cyan');
        } else if (data.state === 'ready') {
            appendLine(terminal, `Captured ${formatBytes(data.file_size)} (~${data.duration}s)`, 'line-green');
            document.getElementById('btn-rec-retransmit').style.display = '';
        } else if (data.state === 'transmitting') {
            appendLine(terminal, `Transmitting iteration #${data.iteration}...`, 'line-amber');
            updateStatusBar(txFreq, 'Retransmitting');
        } else if (data.state === 'complete') {
            appendLine(terminal, 'Retransmission complete.', 'line-green');
            cleanup();
        }
    });
    ws.on('error', (data) => {
        appendLine(terminal, `Error: ${data.message}`, 'line-red');
        toast(data.message || 'Record error', 'error');
        cleanup();
    });

    ws.on('close', () => cleanup());

    ws.connect({
        rx_frequency: rxFreq,
        tx_frequency: txFreq,
        lna_gain: lna,
        vga_gain: vga,
        tx_gain: txGain,
        duration,
        repeat,
    });
}

function retransmit() {
    if (ws) ws.send({ action: 'retransmit' });
    document.getElementById('btn-rec-retransmit').style.display = 'none';
}

function stopRecord() {
    if (ws) ws.close();
    cleanup();
}

function cleanup() {
    if (!running) return;
    running = false;
    ws = null;
    document.getElementById('btn-rec-start').style.display = '';
    document.getElementById('btn-rec-stop').style.display = 'none';
    document.getElementById('btn-rec-retransmit').style.display = 'none';
    updateStatusBar(undefined, '--');
}

function appendLine(el, text, cls = '') {
    const line = document.createElement('div');
    line.className = `line ${cls}`;
    line.textContent = text;
    el.appendChild(line);
    el.scrollTop = el.scrollHeight;
}
