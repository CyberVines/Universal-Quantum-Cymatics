/* ═══════════════════════════════════════════════════════════════════════════
   UQC Web Frontend — App Shell, Router, WebSocket Manager
   ═══════════════════════════════════════════════════════════════════════════ */

// ── Module imports ──────────────────────────────────────────────────────────
import { initTransmit } from './transmit.js';
import { initRawFile } from './rawfile.js';
import { initRecord } from './record.js';
import { initTTS } from './tts.js';
import { initAI } from './ai.js';
import { initAnalyzer } from './analyzer.js';
import { initJitter } from './jitter.js';
import { initLogs } from './logs.js';

// ── Shared Utilities ────────────────────────────────────────────────────────
export function escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
}

export function formatBytes(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / 1048576).toFixed(1) + ' MB';
}

export function bindRange(inputId, valueId) {
    const input = document.getElementById(inputId);
    const span = document.getElementById(valueId);
    if (input && span) {
        input.addEventListener('input', () => { span.textContent = input.value; });
    }
}

// ── Console Logger ──────────────────────────────────────────────────────────
const consoleOutput = document.getElementById('console-output');

export function log(msg, level = 'info') {
    const time = new Date().toLocaleTimeString('en-US', { hour12: false });
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    const cls = { warn: 'log-warn', error: 'log-error', info: 'log-info' }[level] || '';
    entry.innerHTML = `<span class="log-time">${time}</span><span class="${cls}">${escapeHtml(msg)}</span>`;
    if (consoleOutput) {
        consoleOutput.appendChild(entry);
        consoleOutput.scrollTop = consoleOutput.scrollHeight;
    }
}

// ── Toast Notifications ─────────────────────────────────────────────────────
const toastContainer = document.getElementById('toast-container');

export function toast(msg, type = 'info') {
    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.textContent = msg;
    if (toastContainer) toastContainer.appendChild(el);
    setTimeout(() => el.remove(), 4000);
}

// ── Modal ───────────────────────────────────────────────────────────────────
const modalBackdrop = document.getElementById('modal-backdrop');
const modalContent = document.getElementById('modal-content');

export function showModal(html) {
    modalContent.innerHTML = html;
    modalBackdrop.classList.add('visible');
}

export function hideModal() {
    modalBackdrop.classList.remove('visible');
}

modalBackdrop.addEventListener('click', (e) => {
    if (e.target === modalBackdrop) hideModal();
});

// ── API Helper ──────────────────────────────────────────────────────────────
export async function api(path, options = {}) {
    try {
        const { headers: customHeaders, ...rest } = options;
        const headers = { 'Content-Type': 'application/json', ...customHeaders };
        const resp = await fetch(path, { headers, ...rest });
        const data = await resp.json();
        if (!resp.ok) {
            toast(data.error || data.detail || `Error ${resp.status}`, 'error');
            log(`API error: ${path} → ${resp.status}`, 'error');
        }
        return data;
    } catch (err) {
        toast(`Network error: ${err.message}`, 'error');
        log(`Network error: ${path} → ${err.message}`, 'error');
        return null;
    }
}

// ── WebSocket Manager ───────────────────────────────────────────────────────
export class WS {
    constructor(path) {
        this.path = path;
        this.ws = null;
        this.handlers = {};
        this._closed = false;
        this._serverError = false;
        this._config = null;
        this._reconnectAttempts = 0;
        this._maxReconnectAttempts = 5;
        this._reconnectTimer = null;
    }

    on(type, fn) {
        this.handlers[type] = fn;
        return this;
    }

    connect(config) {
        this._closed = false;
        this._serverError = false;
        this._config = config;
        this._reconnectAttempts = 0;
        this._doConnect();
        return this;
    }

    _doConnect() {
        if (this._closed) return;
        const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
        try {
            this.ws = new WebSocket(`${proto}//${location.host}${this.path}`);
        } catch (err) {
            log(`WebSocket creation failed: ${this.path} — ${err.message}`, 'error');
            toast(`Connection failed: ${this.path}`, 'error');
            this._scheduleReconnect();
            return;
        }
        this.ws.onopen = () => {
            this._reconnectAttempts = 0;
            log(`WebSocket connected: ${this.path}`, 'info');
            if (this._config) this.ws.send(JSON.stringify(this._config));
            if (this.handlers.open) this.handlers.open();
        };
        this.ws.onmessage = (e) => {
            try {
                const data = JSON.parse(e.data);
                // Server-side errors should stop reconnection attempts
                if (data.type === 'error') {
                    this._serverError = true;
                }
                const handler = this.handlers[data.type];
                if (handler) handler(data);
            } catch (err) {
                log(`WS parse error: ${err.message}`, 'error');
            }
        };
        this.ws.onclose = (e) => {
            if (this._closed) return;
            log(`WebSocket closed: ${this.path} (code ${e.code})`, 'warn');
            // Don't reconnect if server sent an error or if close was intentional
            if (this._serverError || e.code === 1000 || e.code === 1001) {
                if (this.handlers.close) this.handlers.close();
                return;
            }
            // Only reconnect on network-level failures (1006 = abnormal, no close frame)
            if (e.code === 1006) {
                this._scheduleReconnect();
            } else {
                if (this.handlers.close) this.handlers.close();
            }
        };
        this.ws.onerror = () => {
            // Only log, don't toast — onclose will fire after this and handle cleanup
            log(`WebSocket error: ${this.path}`, 'error');
        };
    }

    _scheduleReconnect() {
        if (this._closed || this._serverError || this._reconnectAttempts >= this._maxReconnectAttempts) {
            if (this._reconnectAttempts >= this._maxReconnectAttempts) {
                log(`WebSocket ${this.path}: max reconnect attempts reached`, 'error');
                toast(`Disconnected: ${this.path.split('/').pop()}`, 'error');
            }
            if (this.handlers.close) this.handlers.close();
            return;
        }
        this._reconnectAttempts++;
        const delay = Math.min(1000 * Math.pow(2, this._reconnectAttempts - 1), 16000);
        log(`WebSocket reconnecting ${this.path} in ${delay}ms (attempt ${this._reconnectAttempts}/${this._maxReconnectAttempts})`, 'warn');
        this._reconnectTimer = setTimeout(() => this._doConnect(), delay);
    }

    send(data) {
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify(data));
        }
    }

    close() {
        this._closed = true;
        this._serverError = false;
        if (this._reconnectTimer) {
            clearTimeout(this._reconnectTimer);
            this._reconnectTimer = null;
        }
        if (this.ws) {
            this.ws.close(1000);
            this.ws = null;
        }
    }
}

// ── Status Bar ──────────────────────────────────────────────────────────────
const hackrfDot = document.getElementById('hackrf-dot');
const hackrfStatus = document.getElementById('hackrf-status');
const activeFreq = document.getElementById('active-freq');
const activeMode = document.getElementById('active-mode');

export function updateStatusBar(freq, mode) {
    if (freq !== undefined) activeFreq.textContent = freq ? `${freq} MHz` : '--';
    if (mode !== undefined) activeMode.textContent = mode || '--';
}

async function pollStatus() {
    try {
        const resp = await fetch('/api/status');
        if (!resp.ok) return;
        const data = await resp.json();
        const detected = data.hackrf_detected;
        const anyActive = Object.values(data.active_processes || {}).some(v => v);

        if (detected && anyActive) {
            hackrfDot.className = 'status-dot warning';
            hackrfStatus.textContent = 'Active';
        } else if (detected) {
            hackrfDot.className = 'status-dot online';
            hackrfStatus.textContent = 'Connected';
        } else {
            hackrfDot.className = 'status-dot offline';
            hackrfStatus.textContent = 'Not found';
        }
    } catch {
        // Server unreachable — silently update status, don't flood console
        hackrfDot.className = 'status-dot offline';
        hackrfStatus.textContent = 'Server offline';
    }
}

// ── Router ──────────────────────────────────────────────────────────────────
const views = document.querySelectorAll('.view');
const navItems = document.querySelectorAll('.nav-item');

function navigate(viewName) {
    views.forEach(v => v.classList.remove('active'));
    navItems.forEach(n => n.classList.remove('active'));

    const target = document.getElementById(`view-${viewName}`);
    const navTarget = document.querySelector(`.nav-item[data-view="${viewName}"]`);
    if (target) target.classList.add('active');
    if (navTarget) navTarget.classList.add('active');

    window.location.hash = viewName;
}

navItems.forEach(item => {
    item.addEventListener('click', () => navigate(item.dataset.view));
});

// ── Console Toggle ──────────────────────────────────────────────────────────
const consolePanel = document.getElementById('console-panel');
const consoleToggle = document.getElementById('console-toggle');
const consoleToggleIcon = document.getElementById('console-toggle-icon');

consoleToggle.addEventListener('click', () => {
    consolePanel.classList.toggle('collapsed');
    consoleToggleIcon.innerHTML = consolePanel.classList.contains('collapsed') ? '&#9650;' : '&#9660;';
});

// ── Init ────────────────────────────────────────────────────────────────────
async function init() {
    log('UQC Web Frontend initializing...', 'info');

    // Load modes
    const modesData = await api('/api/modes');

    // Initialize all feature modules
    initTransmit(modesData?.categories || []);
    initRawFile();
    initRecord();
    initTTS();
    initAI();
    initAnalyzer();
    initJitter();
    initLogs();

    // Handle hash navigation
    const hash = window.location.hash.slice(1);
    if (hash) navigate(hash);

    // Poll status
    pollStatus();
    setInterval(pollStatus, 5000);

    log('Ready.', 'info');
}

init();
