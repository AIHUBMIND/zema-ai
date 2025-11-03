// Zema Dashboard JavaScript
console.log("Zema Dashboard loaded");

// WebSocket connection
let ws = null;

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

// Initialize
document.addEventListener("DOMContentLoaded", () => {
    connectWebSocket();
});
