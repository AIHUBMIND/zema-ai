// Zema Dashboard JavaScript
console.log("Zema Dashboard loaded");

// WebSocket connection
let ws = null;
let logEventSource = null;
let autoScrollEnabled = true;
let liveStreamEnabled = false;

function connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    ws = new WebSocket(wsUrl);
    ws.onopen = () => console.log("WebSocket connected");
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };
    ws.onerror = (error) => console.error("WebSocket error:", error);
    ws.onclose = () => {
        console.log("WebSocket disconnected, reconnecting...");
        setTimeout(connectWebSocket, 3000);
    };
}

function handleWebSocketMessage(data) {
    if (data.type === "status") {
        updateStatus(data.data);
    }
}

function updateStatus(data) {
    const statusEl = document.getElementById("status");
    if (statusEl) {
        statusEl.textContent = data.listening ? "Listening" : "Not Listening";
    }
}

// Logs Viewer Functions
async function loadLogs() {
    const levelFilter = document.getElementById('log-level-filter')?.value || '';
    const searchTerm = document.getElementById('log-search')?.value || '';
    const limit = parseInt(document.getElementById('log-limit')?.value || '100');
    
    const params = new URLSearchParams();
    if (levelFilter) params.append('level', levelFilter);
    if (searchTerm) params.append('search', searchTerm);
    params.append('limit', limit.toString());
    params.append('tail', 'true');
    
    try {
        const response = await fetch(`/api/logs?${params.toString()}`);
        const data = await response.json();
        
        displayLogs(data.logs || []);
        updateLogStats(data);
    } catch (error) {
        console.error('Error loading logs:', error);
        document.getElementById('logs-viewer').innerHTML = 
            `<div class="log-entry error">Error loading logs: ${error.message}</div>`;
    }
}

function displayLogs(logs) {
    const viewer = document.getElementById('logs-viewer');
    if (!viewer) return;
    
    if (logs.length === 0) {
        viewer.innerHTML = '<div class="log-entry">No logs found</div>';
        return;
    }
    
    viewer.innerHTML = logs.map(log => formatLogEntry(log)).join('');
    
    if (autoScrollEnabled) {
        viewer.scrollTop = viewer.scrollHeight;
    }
}

function formatLogEntry(log) {
    const level = log.level || 'INFO';
    const timestamp = log.timestamp || '';
    const message = log.message || '';
    const logger = log.logger || '';
    const module = log.module || '';
    const line = log.line || '';
    
    const levelClass = level.toLowerCase();
    const timeStr = timestamp.split(' ')[1] || timestamp; // Just time part
    
    return `
        <div class="log-entry ${levelClass}">
            <span class="log-time">${timeStr}</span>
            <span class="log-level">${level}</span>
            <span class="log-module">${module || logger}</span>
            <span class="log-message">${escapeHtml(message)}</span>
            ${log.exception ? `<div class="log-exception">${escapeHtml(log.exception)}</div>` : ''}
        </div>
    `;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

async function updateLogStats() {
    try {
        const response = await fetch('/api/logs/stats');
        const stats = await response.json();
        
        const statsEl = document.getElementById('logs-stats');
        if (statsEl && stats.exists) {
            statsEl.innerHTML = `
                <small>
                    File: ${(stats.file_size_mb || 0).toFixed(2)} MB | 
                    Lines: ${stats.total_lines || 0} | 
                    DEBUG: ${stats.level_counts?.DEBUG || 0} | 
                    INFO: ${stats.level_counts?.INFO || 0} | 
                    WARNING: ${stats.level_counts?.WARNING || 0} | 
                    ERROR: ${stats.level_counts?.ERROR || 0} | 
                    CRITICAL: ${stats.level_counts?.CRITICAL || 0}
                </small>
            `;
        }
    } catch (error) {
        console.error('Error loading log stats:', error);
    }
}

function startLiveStream() {
    if (logEventSource) {
        logEventSource.close();
    }
    
    logEventSource = new EventSource('/api/logs/stream');
    
    logEventSource.onmessage = (event) => {
        try {
            const log = JSON.parse(event.data);
            const viewer = document.getElementById('logs-viewer');
            if (viewer) {
                viewer.insertAdjacentHTML('beforeend', formatLogEntry(log));
                if (autoScrollEnabled) {
                    viewer.scrollTop = viewer.scrollHeight;
                }
            }
        } catch (error) {
            console.error('Error parsing log stream:', error);
        }
    };
    
    logEventSource.onerror = (error) => {
        console.error('Log stream error:', error);
        logEventSource.close();
        logEventSource = null;
    };
}

function stopLiveStream() {
    if (logEventSource) {
        logEventSource.close();
        logEventSource = null;
    }
}

async function clearLogs() {
    if (!confirm('Are you sure you want to clear all logs? This cannot be undone.')) {
        return;
    }
    
    try {
        const response = await fetch('/api/logs/clear', { method: 'DELETE' });
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('logs-viewer').innerHTML = 
                '<div class="log-entry info">Logs cleared</div>';
            updateLogStats();
        } else {
            alert('Error clearing logs: ' + (result.message || 'Unknown error'));
        }
    } catch (error) {
        alert('Error clearing logs: ' + error.message);
    }
}

// Navigation handling
function handleNavigation() {
    const sections = document.querySelectorAll('.section');
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = link.getAttribute('href').substring(1);
            
            // Update active nav
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');
            
            // Show target section
            sections.forEach(s => s.classList.remove('active'));
            const targetSection = document.getElementById(target);
            if (targetSection) {
                targetSection.classList.add('active');
            }
            
            // Load logs if navigating to logs section
            if (target === 'logs') {
                loadLogs();
                updateLogStats();
            }
        });
    });
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    connectWebSocket();
    handleNavigation();
    
    // Logs viewer event listeners
    const refreshBtn = document.getElementById('refresh-logs');
    const clearBtn = document.getElementById('clear-logs');
    const levelFilter = document.getElementById('log-level-filter');
    const searchInput = document.getElementById('log-search');
    const limitInput = document.getElementById('log-limit');
    const autoScrollCheck = document.getElementById('auto-scroll');
    const liveStreamCheck = document.getElementById('live-stream');
    
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            stopLiveStream();
            loadLogs();
        });
    }
    
    if (clearBtn) {
        clearBtn.addEventListener('click', clearLogs);
    }
    
    if (levelFilter) {
        levelFilter.addEventListener('change', loadLogs);
    }
    
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', () => {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(loadLogs, 500);
        });
    }
    
    if (limitInput) {
        limitInput.addEventListener('change', loadLogs);
    }
    
    if (autoScrollCheck) {
        autoScrollCheck.addEventListener('change', (e) => {
            autoScrollEnabled = e.target.checked;
        });
    }
    
    if (liveStreamCheck) {
        liveStreamCheck.addEventListener('change', (e) => {
            liveStreamEnabled = e.target.checked;
            if (liveStreamEnabled) {
                startLiveStream();
            } else {
                stopLiveStream();
            }
        });
    }
    
    // Load logs if on logs page
    if (window.location.hash === '#logs' || document.getElementById('logs')?.classList.contains('active')) {
        loadLogs();
        updateLogStats();
    }
});
