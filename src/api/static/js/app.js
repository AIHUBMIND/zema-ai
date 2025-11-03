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
    const statusEl = document.getElementById("status-indicator");
    if (statusEl) {
        statusEl.textContent = data.listening ? "Listening" : "Not Listening";
        statusEl.parentElement.parentElement.className = data.listening ? "small-box bg-success" : "small-box bg-danger";
    }
    
    // Update CPU and Memory
    const cpuEl = document.getElementById("cpu-usage");
    if (cpuEl && data.cpu_percent !== undefined) {
        cpuEl.innerHTML = `${data.cpu_percent.toFixed(1)}<sup style="font-size: 20px">%</sup>`;
    }
    
    const memEl = document.getElementById("memory-usage");
    if (memEl && data.memory_percent !== undefined) {
        memEl.innerHTML = `${data.memory_percent.toFixed(1)}<sup style="font-size: 20px">%</sup>`;
    }
    
    // Update uptime
    const uptimeEl = document.getElementById("uptime-display");
    if (uptimeEl && data.uptime !== undefined) {
        const hours = Math.floor(data.uptime / 3600);
        const minutes = Math.floor((data.uptime % 3600) / 60);
        uptimeEl.textContent = hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;
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

// Navigation handling - Simple and direct approach
function setupNavigation() {
    console.log('🔧 Setting up navigation handlers...');
    
    // Get all sections once
    const sections = document.querySelectorAll('.content-section');
    console.log('Found sections:', sections.length);
    
    // Function to show a specific section
    function showSection(sectionId) {
        console.log('🔄 Showing section:', sectionId);
        
        // Hide ALL sections first
        sections.forEach(s => {
            s.style.display = 'none';
        });
        
        // Show the target section
        const targetSection = document.getElementById(sectionId);
        if (targetSection) {
            targetSection.style.display = 'block';
            console.log('✅ Section displayed:', sectionId);
        } else {
            console.error('❌ Section not found:', sectionId);
            return;
        }
        
        // Update active nav link
        $('.nav-sidebar a').removeClass('active');
        $('.nav-sidebar .nav-item').removeClass('active');
        
        const activeLink = $(`a[data-section="${sectionId}"]`);
        if (activeLink.length) {
            activeLink.addClass('active');
            activeLink.closest('.nav-item').addClass('active');
            console.log('✅ Active link updated:', sectionId);
        }
        
        // Update page title and breadcrumb
        const titles = {
            dashboard: 'Dashboard',
            settings: 'Settings',
            logs: 'Logs',
            users: 'Users',
            history: 'History',
            privacy: 'Privacy',
            'voice-mode': 'Voice Mode'
        };
        const titleEl = document.getElementById('page-title');
        const breadcrumbEl = document.getElementById('breadcrumb-current');
        if (titleEl) titleEl.textContent = titles[sectionId] || 'Dashboard';
        if (breadcrumbEl) breadcrumbEl.textContent = titles[sectionId] || 'Dashboard';
        
        // Load content if needed
        if (sectionId === 'logs') {
            loadLogs();
            updateLogStats();
        } else if (sectionId === 'voice-mode') {
            initVoiceMode();
        } else if (sectionId === 'settings') {
            loadSettings();
        }
    }
    
    // Initialize dropdown voice mode on page load (always available)
    if (typeof initDropdownVoiceMode === 'function') {
        initDropdownVoiceMode();
    }
    
    // Attach click handlers DIRECTLY to each nav link
    // This ensures they work even if AdminLTE interferes
    $('.nav-sidebar a[data-section]').each(function() {
        const $link = $(this);
        const sectionId = $link.attr('data-section');
        
        if (sectionId) {
            // Remove existing handlers and add new one
            $link.off('click.nav').on('click.nav', function(e) {
                e.preventDefault();
                e.stopImmediatePropagation();
                
                console.log('🖱️ Clicked nav link:', sectionId);
                showSection(sectionId);
                window.location.hash = sectionId;
                
                return false; // Prevent any other handlers
            });
        }
    });
    
    // Also handle clicks on the nav-item itself (for clicking icon or text)
    $('.nav-sidebar .nav-item').each(function() {
        const $item = $(this);
        const $link = $item.find('a[data-section]');
        
        if ($link.length) {
            const sectionId = $link.attr('data-section');
            
            $item.off('click.nav').on('click.nav', function(e) {
                // Don't handle if clicking directly on the link (already handled above)
                if ($(e.target).closest('a').length) {
                    return;
                }
                
                e.preventDefault();
                e.stopImmediatePropagation();
                
                console.log('🖱️ Clicked nav item:', sectionId);
                showSection(sectionId);
                window.location.hash = sectionId;
                
                return false;
            });
        }
    });
    
    // Handle hash changes (back/forward browser buttons)
    $(window).on('hashchange', function() {
        const hash = window.location.hash.substring(1) || 'dashboard';
        console.log('🔗 Hash changed:', hash);
        showSection(hash);
    });
    
    // Show initial section based on hash or default to dashboard
    const initialHash = window.location.hash.substring(1) || 'dashboard';
    console.log('🚀 Initial section:', initialHash);
    showSection(initialHash);
    
    console.log('✅ Navigation handlers setup complete');
}

// Load initial status
async function loadInitialStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        updateStatus(data);
    } catch (error) {
        console.error('Error loading initial status:', error);
    }
}

// Initialize - wait for jQuery and AdminLTE to load
$(document).ready(function() {
    console.log('🚀 Initializing Zema Dashboard...');
    
    // Wait a bit for AdminLTE to fully initialize
    setTimeout(function() {
        // Load initial status immediately
        loadInitialStatus();
        
        // Connect WebSocket for real-time updates
        connectWebSocket();
        
        // Setup navigation (uses jQuery internally)
        setupNavigation();
        
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
    
    // Settings management
    setupSettingsHandlers();
    }, 100); // Small delay to ensure AdminLTE is initialized
});

// Settings Management Functions
let currentSettings = {};

async function loadSettings() {
    try {
        const response = await fetch('/api/config/user-facing');
        const settings = await response.json();
        currentSettings = settings;
        
        // Populate form fields
        populateSettingsForm(settings);
    } catch (error) {
        console.error('Error loading settings:', error);
        showSettingsMessage('Error loading settings: ' + error.message, 'danger');
    }
}

function populateSettingsForm(settings) {
    // General
    if (settings.privacy_mode) {
        document.getElementById('privacy-mode').value = settings.privacy_mode;
    }
    if (settings.data_retention_days !== undefined) {
        document.getElementById('data-retention-days').value = settings.data_retention_days;
    }
    if (settings.log_level) {
        document.getElementById('log-level').value = settings.log_level;
    }
    
    // Voice & Audio
    if (settings.wakeword_keywords) {
        const keywords = Array.isArray(settings.wakeword_keywords) 
            ? settings.wakeword_keywords.join(', ') 
            : settings.wakeword_keywords;
        document.getElementById('wakeword-keywords').value = keywords;
    }
    if (settings.wakeword_sensitivity !== undefined) {
        document.getElementById('wakeword-sensitivity').value = settings.wakeword_sensitivity;
        document.getElementById('sensitivity-value').textContent = settings.wakeword_sensitivity;
    }
    if (settings.stt_language) {
        document.getElementById('stt-language').value = settings.stt_language;
    }
    if (settings.tts_voice) {
        document.getElementById('tts-voice').value = settings.tts_voice;
    }
    if (settings.tts_speed !== undefined) {
        document.getElementById('tts-speed').value = settings.tts_speed;
        document.getElementById('speed-value').textContent = settings.tts_speed.toFixed(1) + 'x';
    }
    
    // Camera & Vision
    if (settings.camera_tracking !== undefined) {
        document.getElementById('camera-tracking').checked = settings.camera_tracking;
    }
    if (settings.camera_gestures !== undefined) {
        document.getElementById('camera-gestures').checked = settings.camera_gestures;
    }
    
    // AI & Intelligence
    if (settings.llm_model) {
        document.getElementById('llm-model').value = settings.llm_model;
    }
    if (settings.llm_temperature !== undefined) {
        document.getElementById('llm-temperature').value = settings.llm_temperature;
        document.getElementById('temperature-value').textContent = settings.llm_temperature;
    }
    if (settings.llm_max_tokens !== undefined) {
        document.getElementById('llm-max-tokens').value = settings.llm_max_tokens;
    }
    if (settings.llm_system_prompt) {
        document.getElementById('llm-system-prompt').value = settings.llm_system_prompt;
    }
    
    // Features
    if (settings.feature_voice !== undefined) {
        document.getElementById('feature-voice').checked = settings.feature_voice;
    }
    if (settings.feature_vision !== undefined) {
        document.getElementById('feature-vision').checked = settings.feature_vision;
    }
    if (settings.feature_tasks !== undefined) {
        document.getElementById('feature-tasks').checked = settings.feature_tasks;
    }
    if (settings.feature_ethiopian !== undefined) {
        document.getElementById('feature-ethiopian').checked = settings.feature_ethiopian;
    }
    
    // API Keys (only show if they exist, don't populate for security)
    if (settings.gemini_api_key) {
        document.getElementById('gemini-api-key').value = '••••••••••••••••';
    }
    if (settings.elevenlabs_api_key) {
        document.getElementById('elevenlabs-api-key').value = '••••••••••••••••';
    }
}

function getSettingsFromForm() {
    const settings = {};
    
    // General
    settings.privacy_mode = document.getElementById('privacy-mode').value;
    settings.data_retention_days = parseInt(document.getElementById('data-retention-days').value);
    settings.log_level = document.getElementById('log-level').value;
    
    // Voice & Audio
    const keywordsInput = document.getElementById('wakeword-keywords').value;
    settings.wakeword_keywords = keywordsInput.split(',').map(k => k.trim()).filter(k => k);
    settings.wakeword_sensitivity = parseFloat(document.getElementById('wakeword-sensitivity').value);
    settings.stt_language = document.getElementById('stt-language').value;
    settings.tts_voice = document.getElementById('tts-voice').value;
    settings.tts_speed = parseFloat(document.getElementById('tts-speed').value);
    
    // Camera & Vision
    settings.camera_tracking = document.getElementById('camera-tracking').checked;
    settings.camera_gestures = document.getElementById('camera-gestures').checked;
    
    // AI & Intelligence
    settings.llm_model = document.getElementById('llm-model').value;
    settings.llm_temperature = parseFloat(document.getElementById('llm-temperature').value);
    settings.llm_max_tokens = parseInt(document.getElementById('llm-max-tokens').value);
    settings.llm_system_prompt = document.getElementById('llm-system-prompt').value;
    
    // Features
    settings.feature_voice = document.getElementById('feature-voice').checked;
    settings.feature_vision = document.getElementById('feature-vision').checked;
    settings.feature_tasks = document.getElementById('feature-tasks').checked;
    settings.feature_ethiopian = document.getElementById('feature-ethiopian').checked;
    
    // API Keys (only include if changed)
    const geminiKey = document.getElementById('gemini-api-key').value;
    if (geminiKey && !geminiKey.startsWith('••••')) {
        settings.gemini_api_key = geminiKey;
    }
    
    const elevenlabsKey = document.getElementById('elevenlabs-api-key').value;
    if (elevenlabsKey && !elevenlabsKey.startsWith('••••')) {
        settings.elevenlabs_api_key = elevenlabsKey;
    }
    
    return settings;
}

async function saveSettings() {
    const settings = getSettingsFromForm();
    
    try {
        const response = await fetch('/api/config/bulk', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ updates: settings })
        });
        
        const result = await response.json();
        
        if (result.status === 'success' || result.status === 'partial') {
            showSettingsMessage('Settings saved successfully!', 'success');
            
            // Reload settings to get updated values
            await loadSettings();
            
            // Broadcast update via WebSocket if connected
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    type: 'config_update',
                    data: settings
                }));
            }
        } else {
            showSettingsMessage('Error saving settings: ' + (result.message || 'Unknown error'), 'danger');
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        showSettingsMessage('Error saving settings: ' + error.message, 'danger');
    }
}

function showSettingsMessage(message, type) {
    const messageEl = document.getElementById('settings-message');
    if (messageEl) {
        messageEl.className = `alert alert-${type}`;
        messageEl.textContent = message;
        messageEl.style.display = 'block';
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            messageEl.style.display = 'none';
        }, 5000);
    }
}

function setupSettingsHandlers() {
    // Save button
    const saveBtn = document.getElementById('save-settings');
    if (saveBtn) {
        saveBtn.addEventListener('click', saveSettings);
    }
    
    // Real-time slider updates
    const sensitivitySlider = document.getElementById('wakeword-sensitivity');
    if (sensitivitySlider) {
        sensitivitySlider.addEventListener('input', (e) => {
            document.getElementById('sensitivity-value').textContent = e.target.value;
        });
    }
    
    const speedSlider = document.getElementById('tts-speed');
    if (speedSlider) {
        speedSlider.addEventListener('input', (e) => {
            document.getElementById('speed-value').textContent = parseFloat(e.target.value).toFixed(1) + 'x';
        });
    }
    
    const temperatureSlider = document.getElementById('llm-temperature');
    if (temperatureSlider) {
        temperatureSlider.addEventListener('input', (e) => {
            document.getElementById('temperature-value').textContent = e.target.value;
        });
    }
    
    // Test voice button
    const testVoiceBtn = document.getElementById('test-voice-btn');
    if (testVoiceBtn) {
        testVoiceBtn.addEventListener('click', async () => {
            const voice = document.getElementById('tts-voice').value;
            try {
                // Call TTS API endpoint (if available)
                const response = await fetch('/api/voice/test', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: 'Hello, this is Zema. How can I help you?', voice: voice })
                });
                
                if (response.ok) {
                    showSettingsMessage('Voice test played', 'success');
                } else {
                    showSettingsMessage('Voice test not available yet', 'info');
                }
            } catch (error) {
                showSettingsMessage('Voice test feature coming soon', 'info');
            }
        });
    }
}
