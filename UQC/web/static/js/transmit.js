/* ═══════════════════════════════════════════════════════════════════════════
   Transmit — Compose & Transmit (all 10 mode categories)
   ═══════════════════════════════════════════════════════════════════════════ */
import { api, toast, log, updateStatusBar, bindRange } from './app.js';

// Musical cipher note mapping: A=C4 ... Z=C#6 (chromatic)
const NOTE_NAMES = [
    'C4','C#4','D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4',
    'C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5',
    'C6','C#6',
];

let selectedCategory = null;
let selectedMode = null;

export function initTransmit(categories) {
    const container = document.getElementById('view-transmit');

    container.innerHTML = `
        <h2 class="section-title">Compose &amp; Transmit</h2>

        <div class="form-row">
            <div class="form-group">
                <label>Frequency (MHz)</label>
                <input type="number" id="tx-freq" value="462.700" step="0.001" min="1" max="6000">
            </div>
            <div class="form-group">
                <label>TX Gain (dB)</label>
                <div class="range-row">
                    <input type="range" id="tx-gain" min="0" max="47" value="47">
                    <span class="range-value" id="tx-gain-val">47</span>
                </div>
            </div>
        </div>

        <label>Mode Category</label>
        <div class="mode-grid" id="mode-grid"></div>

        <div class="sub-modes" id="sub-modes"></div>

        <div id="cipher-keyboard-wrap"></div>

        <div class="form-group">
            <label>Message</label>
            <textarea id="tx-message" rows="3" placeholder="Enter your message..."></textarea>
            <div class="char-counter"><span id="tx-char-count">0</span> chars</div>
        </div>

        <div class="param-panel">
            <div class="panel-title">Parameters</div>
            <div class="form-row">
                <div class="form-group">
                    <label>WPM</label>
                    <div class="range-row">
                        <input type="range" id="tx-wpm" min="5" max="60" value="43">
                        <span class="range-value" id="tx-wpm-val">43</span>
                    </div>
                </div>
                <div class="form-group">
                    <label>Tone Freq (Hz)</label>
                    <input type="number" id="tx-tone" value="572" min="100" max="3000">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label>Freq Deviation (Hz)</label>
                    <input type="number" id="tx-fdev" value="5000" min="100" max="75000">
                </div>
                <div class="form-group">
                    <label>Callsign</label>
                    <input type="text" id="tx-callsign" value="N0CALL" maxlength="10">
                </div>
            </div>
        </div>

        <div class="form-row" style="align-items:center">
            <div class="form-group">
                <label>Repeat</label>
                <div class="repeat-control">
                    <input type="number" id="tx-repeat" value="1" min="0" max="9999">
                    <span class="repeat-label">0 = continuous</span>
                </div>
            </div>
        </div>

        <div class="btn-group">
            <button class="btn btn-primary btn-large" id="btn-transmit">TRANSMIT</button>
            <button class="btn btn-danger" id="btn-stop" style="display:none">STOP</button>
        </div>
    `;

    // Build mode category cards
    const grid = document.getElementById('mode-grid');
    categories.forEach(cat => {
        const card = document.createElement('div');
        card.className = 'mode-card';
        card.dataset.catId = cat.id;
        card.innerHTML = `
            <div class="card-title">${cat.id}. ${cat.name}</div>
            <div class="card-desc">${cat.modes.length} mode${cat.modes.length > 1 ? 's' : ''}</div>
        `;
        card.addEventListener('click', () => selectCategory(cat, categories));
        grid.appendChild(card);
    });

    // Range slider live values
    bindRange('tx-gain', 'tx-gain-val');
    bindRange('tx-wpm', 'tx-wpm-val');

    // Character counter
    const msgInput = document.getElementById('tx-message');
    const charCount = document.getElementById('tx-char-count');
    msgInput.addEventListener('input', () => {
        charCount.textContent = msgInput.value.length;
        if (selectedMode === 'MUSIC_CIPHER') {
            highlightCipherKeys(msgInput.value);
        }
    });

    // Transmit button
    document.getElementById('btn-transmit').addEventListener('click', doTransmit);
    document.getElementById('btn-stop').addEventListener('click', doStop);
}

function selectCategory(cat, allCategories) {
    selectedCategory = cat;

    // Highlight card
    document.querySelectorAll('.mode-card').forEach(c => c.classList.remove('selected'));
    document.querySelector(`.mode-card[data-cat-id="${cat.id}"]`).classList.add('selected');

    // Build sub-mode list
    const subModes = document.getElementById('sub-modes');
    if (cat.modes.length === 1) {
        selectedMode = cat.modes[0].id;
        subModes.classList.remove('visible');
        subModes.innerHTML = '';
    } else {
        subModes.classList.add('visible');
        subModes.innerHTML = cat.modes.map(m => `
            <div class="sub-mode-option" data-mode="${m.id}">
                <div class="radio"></div>
                <span>${m.label}</span>
            </div>
        `).join('');

        subModes.querySelectorAll('.sub-mode-option').forEach(opt => {
            opt.addEventListener('click', () => {
                subModes.querySelectorAll('.sub-mode-option').forEach(o => o.classList.remove('selected'));
                opt.classList.add('selected');
                selectedMode = opt.dataset.mode;
            });
        });

        subModes.querySelector('.sub-mode-option').click();
    }

    // Musical cipher keyboard (use == for loose comparison in case of string/number mismatch)
    const kbWrap = document.getElementById('cipher-keyboard-wrap');
    if (cat.id == 10) {
        kbWrap.innerHTML = buildCipherKeyboard();
    } else {
        kbWrap.innerHTML = '';
    }
}

function buildCipherKeyboard() {
    let html = '<label>432 Hz Chromatic Mapping</label><div class="cipher-keyboard">';
    for (let i = 0; i < 26; i++) {
        const letter = String.fromCharCode(65 + i);
        const note = NOTE_NAMES[i];
        const isSharp = note.includes('#');
        html += `<div class="cipher-key ${isSharp ? 'sharp' : ''}" data-letter="${letter}">
            <span>${letter}</span>
            <span class="note">${note}</span>
        </div>`;
    }
    html += '</div>';
    return html;
}

function highlightCipherKeys(text) {
    document.querySelectorAll('.cipher-key').forEach(k => k.classList.remove('active'));
    const upper = text.toUpperCase();
    const lastChar = upper[upper.length - 1];
    if (lastChar && /[A-Z]/.test(lastChar)) {
        const key = document.querySelector(`.cipher-key[data-letter="${lastChar}"]`);
        if (key) key.classList.add('active');
    }
}

function resetTxUI() {
    document.getElementById('btn-transmit').classList.remove('btn-transmitting');
    document.getElementById('btn-stop').style.display = 'none';
}

async function doTransmit() {
    if (!selectedMode) {
        toast('Select a mode first', 'warning');
        return;
    }

    const msg = document.getElementById('tx-message').value.trim();
    if (!msg) {
        toast('Enter a message', 'warning');
        return;
    }

    const freq = parseFloat(document.getElementById('tx-freq').value);
    const wpm = parseInt(document.getElementById('tx-wpm').value);
    const tone = parseInt(document.getElementById('tx-tone').value);
    const fdev = parseInt(document.getElementById('tx-fdev').value);
    const callsign = document.getElementById('tx-callsign').value || 'N0CALL';
    const txGain = parseInt(document.getElementById('tx-gain').value);
    const repeat = parseInt(document.getElementById('tx-repeat').value) || 1;

    document.getElementById('btn-transmit').classList.add('btn-transmitting');
    document.getElementById('btn-stop').style.display = '';

    updateStatusBar(freq, selectedMode);
    log(`Transmitting: ${selectedMode} on ${freq} MHz — "${msg.substring(0, 50)}"`, 'info');

    const result = await api('/api/transmit', {
        method: 'POST',
        body: JSON.stringify({
            mode: selectedMode,
            message: msg,
            frequency: freq,
            wpm, tone_freq: tone, f_dev: fdev,
            callsign, tx_gain: txGain, repeat,
        }),
    });

    if (result?.status === 'transmitting') {
        toast(`Transmitting ${selectedMode}`, 'success');
    } else {
        resetTxUI();
        updateStatusBar(undefined, '--');
    }
}

async function doStop() {
    await api('/api/transmit/stop', { method: 'POST' });
    resetTxUI();
    updateStatusBar(undefined, '--');
    log('Transmission stopped', 'warn');
    toast('Stopped', 'warning');
}
