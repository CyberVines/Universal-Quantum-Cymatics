/* ═══════════════════════════════════════════════════════════════════════════
   RAW File — Transmit a .raw IQ capture file
   ═══════════════════════════════════════════════════════════════════════════ */
import { api, toast, log, updateStatusBar, bindRange, formatBytes } from './app.js';

export function initRawFile() {
    const container = document.getElementById('view-rawfile');

    container.innerHTML = `
        <h2 class="section-title">RAW IQ File Transmit</h2>
        <p class="section-subtitle">Transmit a pre-recorded .raw IQ capture file directly via HackRF.</p>

        <div class="form-row">
            <div class="form-group" style="flex:2">
                <label>File Path</label>
                <input type="text" id="raw-path" placeholder="/path/to/capture.raw">
            </div>
            <div class="form-group">
                <label>Frequency (MHz)</label>
                <input type="number" id="raw-freq" value="462.700" step="0.001">
            </div>
        </div>

        <div class="file-info" id="raw-file-info">
            <div class="info-row">
                <span>File Size:</span>
                <span class="info-value" id="raw-size">--</span>
            </div>
            <div class="info-row">
                <span>Duration:</span>
                <span class="info-value" id="raw-duration">--</span>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>TX Gain (dB)</label>
                <div class="range-row">
                    <input type="range" id="raw-gain" min="0" max="47" value="47">
                    <span class="range-value" id="raw-gain-val">47</span>
                </div>
            </div>
            <div class="form-group">
                <label>Repeat</label>
                <div class="repeat-control">
                    <input type="number" id="raw-repeat" value="1" min="0" max="9999">
                    <span class="repeat-label">0 = continuous</span>
                </div>
            </div>
        </div>

        <div class="btn-group">
            <button class="btn btn-primary btn-large" id="btn-raw-tx">TRANSMIT</button>
            <button class="btn btn-danger" id="btn-raw-stop" style="display:none">STOP</button>
        </div>
    `;

    bindRange('raw-gain', 'raw-gain-val');

    document.getElementById('btn-raw-tx').addEventListener('click', async () => {
        const filePath = document.getElementById('raw-path').value.trim();
        if (!filePath) { toast('Enter a file path', 'warning'); return; }

        const freq = parseFloat(document.getElementById('raw-freq').value);
        const txGain = parseInt(document.getElementById('raw-gain').value);
        const repeat = parseInt(document.getElementById('raw-repeat').value) || 1;

        updateStatusBar(freq, 'RAW File');
        log(`RAW TX: ${filePath} on ${freq} MHz`, 'info');

        document.getElementById('btn-raw-tx').classList.add('btn-transmitting');
        document.getElementById('btn-raw-stop').style.display = '';

        const result = await api('/api/transmit/raw', {
            method: 'POST',
            body: JSON.stringify({
                file_path: filePath,
                frequency: freq,
                tx_gain: txGain,
                repeat,
            }),
        });

        if (result?.status === 'transmitting') {
            toast('Transmitting RAW file', 'success');
            document.getElementById('raw-file-info').classList.add('visible');
            document.getElementById('raw-size').textContent = formatBytes(result.file_size);
            document.getElementById('raw-duration').textContent = `~${result.duration_sec}s`;
        } else {
            resetRawUI();
            updateStatusBar(undefined, '--');
        }
    });

    document.getElementById('btn-raw-stop').addEventListener('click', async () => {
        await api('/api/transmit/stop', { method: 'POST' });
        resetRawUI();
        updateStatusBar(undefined, '--');
        toast('Stopped', 'warning');
    });
}

function resetRawUI() {
    document.getElementById('btn-raw-tx').classList.remove('btn-transmitting');
    document.getElementById('btn-raw-stop').style.display = 'none';
}
