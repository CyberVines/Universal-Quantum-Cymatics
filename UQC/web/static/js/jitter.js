/* ═══════════════════════════════════════════════════════════════════════════
   Jitter Frequency Analysis
   ═══════════════════════════════════════════════════════════════════════════ */
import { WS, toast, log, updateStatusBar, bindRange } from './app.js';

let ws = null;
let running = false;

export function initJitter() {
    const container = document.getElementById('view-jitter');

    container.innerHTML = `
        <h2 class="section-title">Jitter Frequency Analysis</h2>
        <p class="section-subtitle">Capture RF, extract peaks (1) and valleys (0) as binary, then run through ciphers, gematria, and math anomaly detection. Results are auto-logged.</p>

        <div class="form-row">
            <div class="form-group">
                <label>Frequency (MHz)</label>
                <input type="number" id="jf-freq" value="462.700" step="0.001">
            </div>
            <div class="form-group">
                <label>Demod Mode</label>
                <select id="jf-demod">
                    <option value="DEMOD_NBFM" data-label="NBFM">NBFM</option>
                    <option value="DEMOD_WBFM" data-label="WBFM">WBFM</option>
                    <option value="DEMOD_AM" data-label="AM">AM</option>
                    <option value="DEMOD_USB" data-label="USB">USB</option>
                    <option value="DEMOD_LSB" data-label="LSB">LSB</option>
                </select>
            </div>
            <div class="form-group">
                <label>Listen Duration (sec)</label>
                <input type="number" id="jf-listen" value="13.7" step="0.1" min="0.1" max="120">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>LNA Gain</label>
                <div class="range-row">
                    <input type="range" id="jf-lna" min="0" max="40" step="8" value="16">
                    <span class="range-value" id="jf-lna-val">16</span>
                </div>
            </div>
            <div class="form-group">
                <label>VGA Gain</label>
                <div class="range-row">
                    <input type="range" id="jf-vga" min="0" max="62" step="2" value="20">
                    <span class="range-value" id="jf-vga-val">20</span>
                </div>
            </div>
        </div>

        <div class="btn-group">
            <button class="btn btn-primary btn-large" id="btn-jf-start">START</button>
            <button class="btn btn-danger btn-large" id="btn-jf-stop" style="display:none">STOP</button>
        </div>

        <div style="margin-top:16px;display:flex;align-items:center;gap:12px">
            <label style="margin:0">Session ID:</label>
            <span id="jf-session" style="color:var(--cyan);font-size:12px">--</span>
            <span style="font-size:10px;color:var(--text-dim);margin-left:auto">Results auto-logged to anomaly repository</span>
        </div>

        <label style="margin-top:12px">Analysis Output</label>
        <div class="terminal" id="jf-terminal" style="margin-top:8px;min-height:200px;max-height:600px"></div>
    `;

    bindRange('jf-lna', 'jf-lna-val');
    bindRange('jf-vga', 'jf-vga-val');

    document.getElementById('btn-jf-start').addEventListener('click', start);
    document.getElementById('btn-jf-stop').addEventListener('click', stop);
}

function start() {
    if (running) return;
    running = true;

    const freq = parseFloat(document.getElementById('jf-freq').value);
    const demodSelect = document.getElementById('jf-demod');
    const demodLabel = demodSelect.options[demodSelect.selectedIndex].dataset.label;
    const terminal = document.getElementById('jf-terminal');
    terminal.textContent = '';

    document.getElementById('btn-jf-start').style.display = 'none';
    document.getElementById('btn-jf-stop').style.display = '';
    document.getElementById('jf-session').textContent = 'Starting...';

    updateStatusBar(freq, 'Jitter');
    log(`Jitter Analysis started on ${freq} MHz (${demodLabel})`, 'info');

    ws = new WS('/ws/jitter');

    ws.on('session', (data) => {
        document.getElementById('jf-session').textContent = data.session_id || '--';
    });

    ws.on('status', (data) => {
        const labels = {
            listening: 'Capturing...',
            demodulating: 'Demodulating...',
            analyzing: 'Analyzing peaks/valleys...',
            no_data: 'No data captured',
            demod_failed: 'Demodulation failed',
        };
        appendLine(terminal, `[Round ${data.round}] ${labels[data.state] || data.state}`, 'line-dim');
    });

    ws.on('result', (data) => {
        if (data.output) {
            appendLine(terminal, `══ Round ${data.round} ══`, 'line-cyan');
            data.output.split('\n').forEach(line => {
                let cls = '';
                if (line.includes('ANOMALY') || line.includes('CRITICAL')) cls = 'line-red';
                else if (line.includes('NOTABLE') || line.includes('Match')) cls = 'line-amber';
                else if (line.includes('Binary') || line.includes('Peaks')) cls = 'line-green';
                appendLine(terminal, line, cls);
            });
        }
        if (data.error) {
            appendLine(terminal, data.error, 'line-red');
        }
        appendLine(terminal, '');
    });

    ws.on('error', (data) => {
        appendLine(terminal, `ERROR: ${data.message}`, 'line-red');
        toast(data.message || 'Jitter error', 'error');
        cleanup();
    });

    ws.on('close', () => cleanup());

    ws.connect({
        demod: demodSelect.value,
        demod_label: demodLabel,
        frequency: freq,
        listen_sec: parseFloat(document.getElementById('jf-listen').value),
        lna_gain: parseInt(document.getElementById('jf-lna').value),
        vga_gain: parseInt(document.getElementById('jf-vga').value),
    });
}

function stop() {
    if (ws) ws.close();
    cleanup();
    log('Jitter Analysis stopped', 'warn');
    toast('Jitter Analysis stopped', 'warning');
}

function cleanup() {
    if (!running) return;
    running = false;
    ws = null;
    document.getElementById('btn-jf-start').style.display = '';
    document.getElementById('btn-jf-stop').style.display = 'none';
    updateStatusBar(undefined, '--');
}

function appendLine(el, text, cls = '') {
    const line = document.createElement('div');
    line.className = `line ${cls}`;
    line.textContent = text;
    el.appendChild(line);
    el.scrollTop = el.scrollHeight;
}
