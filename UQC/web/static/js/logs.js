/* ═══════════════════════════════════════════════════════════════════════════
   Anomaly Repository / Event Viewer
   ═══════════════════════════════════════════════════════════════════════════ */
import { api, toast, log, showModal, hideModal } from './app.js';

const CATEGORIES = ['_', 'SYSTEM', 'SIGNAL', 'CIPHER', 'GEMATRIA', 'MATH', 'WORD', 'PATTERN', 'MUSIC'];
const SEVERITIES = ['_', 'CRITICAL', 'ANOMALY', 'NOTABLE', 'INFO'];

export function initLogs() {
    const container = document.getElementById('view-logs');

    const catOpts = CATEGORIES.map(c => `<option value="${c}">${c === '_' ? 'All' : c}</option>`).join('');
    const sevOpts = SEVERITIES.map(s => `<option value="${s}">${s === '_' ? 'All' : s}</option>`).join('');

    container.innerHTML = `
        <h2 class="section-title">Anomaly Repository</h2>

        <div id="log-stats" class="stats-grid" style="margin-bottom:20px"></div>

        <div class="filter-bar">
            <div class="form-group">
                <label>Category</label>
                <select id="log-cat">${catOpts}</select>
            </div>
            <div class="form-group">
                <label>Severity</label>
                <select id="log-sev">${sevOpts}</select>
            </div>
            <div class="form-group search-group">
                <label>Search</label>
                <input type="text" id="log-search" placeholder="Search text...">
            </div>
            <div class="form-group" style="min-width:80px">
                <label>Limit</label>
                <input type="number" id="log-limit" value="50" min="1" max="500">
            </div>
            <button class="btn btn-cyan" id="btn-log-query" style="align-self:flex-end;margin-bottom:0">Search</button>
        </div>

        <div class="terminal" id="log-output" style="min-height:200px;max-height:500px;color:var(--text)"></div>

        <div class="btn-group" style="margin-top:16px">
            <button class="btn" id="btn-log-stats">Refresh Stats</button>
            <button class="btn btn-cyan" id="btn-export-text">Export Text</button>
            <button class="btn btn-cyan" id="btn-export-json">Export JSON</button>
            <button class="btn btn-cyan" id="btn-export-csv">Export CSV</button>
            <button class="btn btn-danger" id="btn-log-clear">Archive &amp; Clear</button>
        </div>

        <div id="log-export-result" style="margin-top:12px"></div>
    `;

    // Query
    document.getElementById('btn-log-query').addEventListener('click', queryLogs);

    // Stats
    document.getElementById('btn-log-stats').addEventListener('click', loadStats);

    // Export buttons
    document.getElementById('btn-export-text').addEventListener('click', () => exportLogs('text'));
    document.getElementById('btn-export-json').addEventListener('click', () => exportLogs('json'));
    document.getElementById('btn-export-csv').addEventListener('click', () => exportLogs('csv'));

    // Clear
    document.getElementById('btn-log-clear').addEventListener('click', confirmClear);

    // Initial load
    loadStats();
    queryLogs();
}

async function queryLogs() {
    const cat = document.getElementById('log-cat').value;
    const sev = document.getElementById('log-sev').value;
    const search = document.getElementById('log-search').value.trim() || '_';
    const limit = parseInt(document.getElementById('log-limit').value) || 50;

    const output = document.getElementById('log-output');
    output.textContent = 'Querying...';

    const params = new URLSearchParams({ category: cat, severity: sev, search, limit });
    const result = await api(`/api/logs?${params}`);

    if (result) {
        const text = result.output || '(no results)';
        output.textContent = '';
        text.split('\n').forEach(line => {
            const el = document.createElement('div');
            el.className = 'line';
            if (line.includes('CRITICAL')) el.className += ' line-red';
            else if (line.includes('ANOMALY')) el.className += ' line-amber';
            else if (line.includes('NOTABLE')) el.className += ' line-cyan';
            else if (line.includes('───') || line.includes('═══')) el.className += ' line-dim';
            el.textContent = line;
            output.appendChild(el);
        });
    }
}

async function loadStats() {
    const result = await api('/api/logs/stats');
    const statsEl = document.getElementById('log-stats');

    if (result?.output) {
        // Parse stats output into cards
        const lines = result.output.split('\n').filter(l => l.trim());
        const counts = {};
        let total = 0;

        lines.forEach(line => {
            const match = line.match(/(\w+)\s*[:=]\s*(\d+)/);
            if (match) {
                counts[match[1]] = parseInt(match[2]);
                total += parseInt(match[2]);
            }
        });

        // If we got counts, render them as cards
        if (Object.keys(counts).length > 0) {
            statsEl.innerHTML = Object.entries(counts).map(([key, val]) => {
                let cls = '';
                if (key === 'CRITICAL') cls = 'red';
                else if (key === 'ANOMALY') cls = 'amber';
                else if (key === 'NOTABLE') cls = 'cyan';
                return `<div class="stat-card ${cls}">
                    <div class="stat-value">${val}</div>
                    <div class="stat-label">${key}</div>
                </div>`;
            }).join('');
        } else {
            // Show raw output
            statsEl.innerHTML = `<div class="stat-card"><div class="stat-value" style="font-size:12px;white-space:pre-wrap;text-align:left;color:var(--text)">${escapeHtml(result.output)}</div></div>`;
        }
    } else {
        statsEl.innerHTML = '<div class="stat-card"><div class="stat-label">No stats available</div></div>';
    }
}

async function exportLogs(format) {
    log(`Exporting logs as ${format}...`, 'info');
    const result = await api('/api/logs/export', {
        method: 'POST',
        body: JSON.stringify({ format }),
    });

    const exportResult = document.getElementById('log-export-result');
    if (result?.file) {
        exportResult.innerHTML = `<span style="color:var(--green);font-size:12px">Exported to: ${escapeHtml(result.file)}</span>`;
        toast(`Exported as ${format}`, 'success');
    } else {
        exportResult.innerHTML = `<span style="color:var(--red);font-size:12px">Export failed</span>`;
    }
}

function confirmClear() {
    showModal(`
        <h3>Archive &amp; Clear Logs</h3>
        <p>This will archive current logs and clear the repository. This action cannot be undone.</p>
        <div class="btn-group">
            <button class="btn btn-danger" id="btn-confirm-clear">Archive &amp; Clear</button>
            <button class="btn" id="btn-cancel-clear">Cancel</button>
        </div>
    `);

    document.getElementById('btn-confirm-clear').addEventListener('click', async () => {
        hideModal();
        const result = await api('/api/logs/clear', {
            method: 'POST',
            body: JSON.stringify({ no_archive: false }),
        });
        toast('Logs archived and cleared', 'success');
        log('Logs archived and cleared', 'warn');
        loadStats();
        queryLogs();
    });

    document.getElementById('btn-cancel-clear').addEventListener('click', hideModal);
}

function escapeHtml(text) {
    const d = document.createElement('div');
    d.textContent = text;
    return d.innerHTML;
}
