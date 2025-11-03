// Voice Mode Functions
let voiceWebSocket = null;
let mediaRecorder = null;
let audioStream = null;
let isRecording = false;
let conversationHistory = [];

// Voice Mode State Management
function setVoiceState(state) {
    // Update full page voice mode
    const indicator = document.getElementById('voice-indicator');
    const status = document.getElementById('voice-status');
    const icon = document.getElementById('voice-icon');
    const startBtn = document.getElementById('voice-start');
    const stopBtn = document.getElementById('voice-stop');
    
    if (indicator) {
        indicator.classList.remove('idle', 'listening', 'speaking', 'processing');
        indicator.classList.add(state);
    }
    
    if (status) {
        const statusText = {
            'idle': 'Ready to listen',
            'listening': 'Listening...',
            'processing': 'Processing...',
            'speaking': 'Speaking...'
        };
        status.textContent = statusText[state] || 'Ready';
    }
    
    if (icon) {
        const iconClass = {
            'idle': 'fas fa-microphone',
            'listening': 'fas fa-microphone',
            'processing': 'fas fa-cog',
            'speaking': 'fas fa-volume-up'
        };
        icon.className = iconClass[state] + ' voice-mode-icon';
    }
    
    if (startBtn) {
        startBtn.disabled = (state !== 'idle');
        startBtn.classList.toggle('active', state === 'listening');
    }
    
    if (stopBtn) {
        stopBtn.disabled = (state === 'idle');
    }
    
    // Update dropdown voice mode
    const dropdownIndicator = document.getElementById('voice-dropdown-indicator');
    const dropdownStatus = document.getElementById('voice-dropdown-status');
    const dropdownIcon = document.getElementById('voice-dropdown-icon');
    const dropdownStartBtn = document.getElementById('voice-dropdown-start');
    const dropdownStopBtn = document.getElementById('voice-dropdown-stop');
    const voiceBadge = document.getElementById('voice-status-badge');
    
    if (dropdownIndicator) {
        dropdownIndicator.classList.remove('idle', 'listening', 'speaking', 'processing');
        dropdownIndicator.classList.add(state);
    }
    
    if (dropdownStatus) {
        const statusText = {
            'idle': 'Ready to listen',
            'listening': 'Listening...',
            'processing': 'Processing...',
            'speaking': 'Speaking...'
        };
        dropdownStatus.textContent = statusText[state] || 'Ready';
    }
    
    if (dropdownIcon) {
        const iconClass = {
            'idle': 'fas fa-microphone',
            'listening': 'fas fa-microphone',
            'processing': 'fas fa-cog',
            'speaking': 'fas fa-volume-up'
        };
        dropdownIcon.className = iconClass[state] || 'fas fa-microphone';
    }
    
    if (dropdownStartBtn) {
        dropdownStartBtn.disabled = (state !== 'idle');
    }
    
    if (dropdownStopBtn) {
        dropdownStopBtn.disabled = (state === 'idle');
    }
    
    // Show badge when active
    if (voiceBadge) {
        voiceBadge.style.display = (state !== 'idle') ? 'inline-block' : 'none';
    }
}

// Initialize Voice Mode
function initVoiceMode() {
    console.log('🎤 Initializing Voice Mode...');
    
    const startBtn = document.getElementById('voice-start');
    const stopBtn = document.getElementById('voice-stop');
    const clearBtn = document.getElementById('voice-clear');
    const screenshotBtn = document.getElementById('voice-screenshot');
    const cameraBtn = document.getElementById('voice-camera');
    
    if (startBtn) {
        startBtn.addEventListener('click', startVoiceRecording);
    }
    
    if (stopBtn) {
        stopBtn.addEventListener('click', stopVoiceRecording);
    }
    
    if (clearBtn) {
        clearBtn.addEventListener('click', clearTranscript);
    }
    
    if (screenshotBtn) {
        screenshotBtn.addEventListener('click', captureScreen);
    }
    
    if (cameraBtn) {
        cameraBtn.addEventListener('click', toggleCamera);
    }
    
    // Initialize dropdown voice mode
    initDropdownVoiceMode();
    
    setVoiceState('idle');
}

// Initialize Dropdown Voice Mode
function initDropdownVoiceMode() {
    console.log('🎤 Initializing Dropdown Voice Mode...');
    
    const dropdownStartBtn = document.getElementById('voice-dropdown-start');
    const dropdownStopBtn = document.getElementById('voice-dropdown-stop');
    const dropdownClearBtn = document.getElementById('voice-dropdown-clear');
    const dropdownScreenshotBtn = document.getElementById('voice-dropdown-screenshot');
    const dropdownCloseBtn = document.getElementById('voice-dropdown-close');
    
    if (dropdownStartBtn) {
        dropdownStartBtn.addEventListener('click', startVoiceRecording);
    }
    
    if (dropdownStopBtn) {
        dropdownStopBtn.addEventListener('click', stopVoiceRecording);
    }
    
    if (dropdownClearBtn) {
        dropdownClearBtn.addEventListener('click', clearTranscript);
    }
    
    if (dropdownScreenshotBtn) {
        dropdownScreenshotBtn.addEventListener('click', captureScreen);
    }
    
    if (dropdownCloseBtn) {
        dropdownCloseBtn.addEventListener('click', () => {
            $('#voice-dropdown').dropdown('hide');
        });
    }
    
    // Keep dropdown open when clicking inside
    $(document).on('click', '.voice-dropdown', function(e) {
        e.stopPropagation();
    });
}

// Start Voice Recording
async function startVoiceRecording() {
    try {
        console.log('🎤 Starting voice recording...');
        
        // Request microphone access
        audioStream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
                sampleRate: 16000
            } 
        });
        
        // Connect to voice WebSocket
        const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
        voiceWebSocket = new WebSocket(`${protocol}//${window.location.host}/ws/voice`);
        
        voiceWebSocket.onopen = () => {
            console.log('✅ Voice WebSocket connected');
            setVoiceState('listening');
            isRecording = true;
            
            // Start MediaRecorder
            mediaRecorder = new MediaRecorder(audioStream, {
                mimeType: 'audio/webm;codecs=opus'
            });
            
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0 && voiceWebSocket.readyState === WebSocket.OPEN) {
                    voiceWebSocket.send(event.data);
                }
            };
            
            mediaRecorder.start(100); // Send chunks every 100ms
        };
        
        voiceWebSocket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                handleVoiceMessage(data);
            } catch (e) {
                console.error('Error parsing voice message:', e);
            }
        };
        
        voiceWebSocket.onerror = (error) => {
            console.error('Voice WebSocket error:', error);
            setVoiceState('idle');
            stopVoiceRecording();
        };
        
        voiceWebSocket.onclose = () => {
            console.log('Voice WebSocket closed');
            setVoiceState('idle');
            stopVoiceRecording();
        };
        
    } catch (error) {
        console.error('Error starting voice recording:', error);
        alert('Could not access microphone. Please check permissions.');
        setVoiceState('idle');
    }
}

// Stop Voice Recording
function stopVoiceRecording() {
    console.log('🛑 Stopping voice recording...');
    
    isRecording = false;
    
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
    }
    
    if (audioStream) {
        audioStream.getTracks().forEach(track => track.stop());
        audioStream = null;
    }
    
    if (voiceWebSocket) {
        voiceWebSocket.close();
        voiceWebSocket = null;
    }
    
    setVoiceState('idle');
}

// Handle Voice Messages
function handleVoiceMessage(data) {
    const transcriptEl = document.getElementById('voice-transcript');
    
    switch(data.type) {
        case 'transcript':
            // User speech transcript
            addToTranscript(data.text, 'user');
            setVoiceState('processing');
            break;
            
        case 'response':
            // Assistant response
            addToTranscript(data.text, 'assistant');
            setVoiceState('speaking');
            
            // Speak the response
            speakText(data.text);
            break;
            
        case 'status':
            // Status updates
            if (data.status === 'listening') {
                setVoiceState('listening');
            } else if (data.status === 'processing') {
                setVoiceState('processing');
            }
            break;
            
        case 'error':
            console.error('Voice error:', data.message);
            addToTranscript(`Error: ${data.message}`, 'error');
            setVoiceState('idle');
            break;
    }
}

// Initialize Dropdown Voice Mode
function initDropdownVoiceMode() {
    console.log('🎤 Initializing Dropdown Voice Mode...');
    
    const dropdownStartBtn = document.getElementById('voice-dropdown-start');
    const dropdownStopBtn = document.getElementById('voice-dropdown-stop');
    const dropdownClearBtn = document.getElementById('voice-dropdown-clear');
    const dropdownScreenshotBtn = document.getElementById('voice-dropdown-screenshot');
    const dropdownCloseBtn = document.getElementById('voice-dropdown-close');
    
    if (dropdownStartBtn) {
        dropdownStartBtn.addEventListener('click', startVoiceRecording);
    }
    
    if (dropdownStopBtn) {
        dropdownStopBtn.addEventListener('click', stopVoiceRecording);
    }
    
    if (dropdownClearBtn) {
        dropdownClearBtn.addEventListener('click', clearTranscript);
    }
    
    if (dropdownScreenshotBtn) {
        dropdownScreenshotBtn.addEventListener('click', captureScreen);
    }
    
    if (dropdownCloseBtn) {
        dropdownCloseBtn.addEventListener('click', () => {
            $('#voice-dropdown').dropdown('hide');
        });
    }
    
    // Keep dropdown open when clicking inside
    $(document).on('click', '.voice-dropdown', function(e) {
        e.stopPropagation();
    });
}

// Add to Transcript
function addToTranscript(text, type = 'user') {
    // Full page transcript
    const transcriptEl = document.getElementById('voice-transcript');
    if (transcriptEl) {
        const existingContent = transcriptEl.innerHTML;
        
        if (existingContent.includes('Your conversation will appear here')) {
            transcriptEl.innerHTML = '';
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `mb-2 ${type === 'user' ? 'text-primary' : type === 'assistant' ? 'text-success' : 'text-danger'}`;
        messageDiv.innerHTML = `<strong>${type === 'user' ? 'You' : type === 'assistant' ? 'Zema' : 'Error'}:</strong> ${escapeHtml(text)}`;
        
        transcriptEl.appendChild(messageDiv);
        transcriptEl.scrollTop = transcriptEl.scrollHeight;
    }
    
    // Dropdown transcript
    const dropdownTranscriptEl = document.getElementById('voice-dropdown-transcript');
    if (dropdownTranscriptEl) {
        const existingContent = dropdownTranscriptEl.innerHTML;
        
        if (existingContent.includes('Your conversation will appear here')) {
            dropdownTranscriptEl.innerHTML = '';
        }
        
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.innerHTML = `<strong>${type === 'user' ? 'You' : type === 'assistant' ? 'Zema' : 'Error'}:</strong> ${escapeHtml(text)}`;
        
        dropdownTranscriptEl.appendChild(messageDiv);
        dropdownTranscriptEl.scrollTop = dropdownTranscriptEl.scrollHeight;
    }
    
    conversationHistory.push({ type, text, timestamp: new Date() });
}

// Clear Transcript
function clearTranscript() {
    const transcriptEl = document.getElementById('voice-transcript');
    const dropdownTranscriptEl = document.getElementById('voice-dropdown-transcript');
    
    if (transcriptEl) {
        transcriptEl.innerHTML = '<div class="text-muted text-center">Your conversation will appear here...</div>';
    }
    
    if (dropdownTranscriptEl) {
        dropdownTranscriptEl.innerHTML = '<div class="text-muted text-center small">Your conversation will appear here...</div>';
    }
    
    conversationHistory = [];
}

// Speak Text (using Web Speech API)
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        utterance.onstart = () => {
            setVoiceState('speaking');
        };
        
        utterance.onend = () => {
            setVoiceState('listening');
        };
        
        speechSynthesis.speak(utterance);
    } else {
        console.warn('Speech synthesis not supported');
        setVoiceState('listening');
    }
}

// Capture Screen
async function captureScreen() {
    try {
        const stream = await navigator.mediaDevices.getDisplayMedia({
            video: { mediaSource: 'screen' }
        });
        
        // Take screenshot
        const video = document.createElement('video');
        video.srcObject = stream;
        video.play();
        
        video.onloadedmetadata = () => {
            const canvas = document.createElement('canvas');
            canvas.width = video.videoWidth;
            canvas.height = video.videoHeight;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(video, 0, 0);
            
            canvas.toBlob((blob) => {
                // Send to backend
                sendScreenCapture(blob);
                
                // Stop stream
                stream.getTracks().forEach(track => track.stop());
            });
        };
        
    } catch (error) {
        console.error('Error capturing screen:', error);
        alert('Could not capture screen. Please check permissions.');
    }
}

// Send Screen Capture
async function sendScreenCapture(blob) {
    try {
        const formData = new FormData();
        formData.append('screenshot', blob, 'screenshot.png');
        
        const response = await fetch('/api/vision/screenshot', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        console.log('Screen captured:', data);
        addToTranscript('Screen captured and sent to Zema', 'info');
    } catch (error) {
        console.error('Error sending screenshot:', error);
    }
}

// Escape HTML helper
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize dropdown on page load
$(document).ready(function() {
    initDropdownVoiceMode();
});

