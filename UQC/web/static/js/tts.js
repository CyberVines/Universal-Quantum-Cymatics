/* ═══════════════════════════════════════════════════════════════════════════
   TTS — Text-to-Speech Transmit
   ═══════════════════════════════════════════════════════════════════════════ */
import { api, toast, log, updateStatusBar, bindRange } from './app.js';

export function initTTS() {
    const container = document.getElementById('view-tts');

    container.innerHTML = `
        <h2 class="section-title">Text-to-Speech Transmit</h2>
        <p class="section-subtitle">Generate speech via espeak-ng, modulate, and transmit over HackRF.</p>

        <div class="form-row">
            <div class="form-group">
                <label>Frequency (MHz)</label>
                <input type="number" id="tts-freq" value="462.700" step="0.001">
            </div>
            <div class="form-group">
                <label>Modulation</label>
                <select id="tts-mod">
                    <option value="WAV_NBFM">NBFM (+/-5 kHz)</option>
                    <option value="WAV_WBFM">WBFM (+/-75 kHz)</option>
                    <option value="WAV_AM">AM</option>
                    <option value="WAV_USB">USB</option>
                    <option value="WAV_LSB">LSB</option>
                </select>
            </div>
        </div>

        <div class="form-group">
            <label>Message</label>
            <textarea id="tts-message" rows="4" placeholder="Enter text to speak..."></textarea>
        </div>

        <div class="param-panel">
            <div class="panel-title">Voice Configuration</div>
            <div class="form-row">
                <div class="form-group">
                    <label>Language / Voice</label>
                    <select id="tts-voice">
                        <option value="en">English</option>
                        <option value="en-us">English (US)</option>
                        <option value="en-gb">English (GB)</option>
                        <option value="es">Spanish</option>
                        <option value="fr">French</option>
                        <option value="de">German</option>
                        <option value="ru">Russian</option>
                        <option value="zh">Chinese</option>
                        <option value="ja">Japanese</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Speed (WPM)</label>
                    <div class="range-row">
                        <input type="range" id="tts-speed" min="50" max="400" value="150">
                        <span class="range-value" id="tts-speed-val">150</span>
                    </div>
                </div>
                <div class="form-group">
                    <label>Word Gap</label>
                    <div class="range-row">
                        <input type="range" id="tts-gap" min="1" max="50" value="5">
                        <span class="range-value" id="tts-gap-val">5</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>TX Gain (dB)</label>
                <div class="range-row">
                    <input type="range" id="tts-gain" min="0" max="47" value="47">
                    <span class="range-value" id="tts-gain-val">47</span>
                </div>
            </div>
            <div class="form-group">
                <label>Repeat</label>
                <div class="repeat-control">
                    <input type="number" id="tts-repeat" value="1" min="0" max="9999">
                    <span class="repeat-label">0 = continuous</span>
                </div>
            </div>
        </div>

        <div class="btn-group">
            <button class="btn btn-primary btn-large" id="btn-tts-tx">TRANSMIT</button>
            <button class="btn btn-danger" id="btn-tts-stop" style="display:none">STOP</button>
        </div>
    `;

    bindRange('tts-speed', 'tts-speed-val');
    bindRange('tts-gap', 'tts-gap-val');
    bindRange('tts-gain', 'tts-gain-val');

    document.getElementById('btn-tts-tx').addEventListener('click', async () => {
        const msg = document.getElementById('tts-message').value.trim();
        if (!msg) { toast('Enter a message', 'warning'); return; }

        const freq = parseFloat(document.getElementById('tts-freq').value);
        const mod = document.getElementById('tts-mod').value;
        const voice = document.getElementById('tts-voice').value;
        const speed = parseInt(document.getElementById('tts-speed').value);
        const gap = parseInt(document.getElementById('tts-gap').value);
        const txGain = parseInt(document.getElementById('tts-gain').value);
        const repeat = parseInt(document.getElementById('tts-repeat').value) || 1;

        updateStatusBar(freq, `TTS ${mod.replace('WAV_', '')}`);
        log(`TTS TX: ${mod} on ${freq} MHz — "${msg.substring(0, 40)}"`, 'info');

        document.getElementById('btn-tts-tx').classList.add('btn-transmitting');
        document.getElementById('btn-tts-stop').style.display = '';

        const result = await api('/api/tts', {
            method: 'POST',
            body: JSON.stringify({
                message: msg,
                frequency: freq,
                modulation: mod,
                voice, speed, word_gap: gap,
                tx_gain: txGain, repeat,
            }),
        });

        if (result?.status === 'transmitting') {
            toast('TTS transmitting', 'success');
        } else {
            resetTtsUI();
            updateStatusBar(undefined, '--');
        }
    });

    document.getElementById('btn-tts-stop').addEventListener('click', async () => {
        await api('/api/transmit/stop', { method: 'POST' });
        resetTtsUI();
        updateStatusBar(undefined, '--');
        toast('Stopped', 'warning');
    });
}

function resetTtsUI() {
    document.getElementById('btn-tts-tx').classList.remove('btn-transmitting');
    document.getElementById('btn-tts-stop').style.display = 'none';
}
