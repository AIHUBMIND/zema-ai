# Smart Hybrid Mode - Connectivity Detection Design

**Purpose:** Design document for automatic Internet connectivity detection and hybrid mode switching  
**Status:** Design Phase - To be implemented in SETUP-004 or later  
**Last Updated:** 2025-11-03

---

## 🎯 Requirement

**User Requirement:**
> "Whenever there is an Internet connection to Wi-Fi, as long as there is active Internet, I need this AI assistant to use the Internet because it cannot beat the live connection to real data than disconnected data. So the application should know if there is no Internet - still works using the local LLM - then when Internet connection is there, I want it to connect to the Internet back and temporarily stop using the local LLM."

**Summary:**
- **Internet Available:** Use online services (preferred for better accuracy)
- **Internet Unavailable:** Fall back to local LLM (offline mode)
- **Dynamic Switching:** Automatically detect and switch modes without user intervention

---

## 🏗️ Architecture

### Connection Modes

1. **`auto` (Default) - Smart Hybrid Mode**
   - Automatically detects Internet connectivity
   - Uses online services when available
   - Falls back to local LLM when offline
   - Seamless switching

2. **`local` - Offline-Only Mode**
   - Always uses local LLM
   - Never attempts Internet connection
   - 100% privacy mode

3. **`online` - Online-Only Mode**
   - Always attempts to use online services
   - Requires Internet connection
   - Falls back to local LLM if Internet unavailable

---

## 🔍 Connectivity Detection

### Detection Strategy

**Periodic Health Checks:**
- Check Internet connectivity every 30 seconds (configurable)
- Use lightweight HTTP request to reliable endpoint
- Cache connectivity status
- Update status on-demand before critical operations

**Detection Endpoints:**
- Primary: `https://www.google.com` (configurable via `INTERNET_CHECK_URL`)
- Fallback: `https://cloudflare.com` or `https://github.com`
- Timeout: 3 seconds max per check

**Detection Logic:**
```python
async def check_internet_connectivity() -> bool:
    """
    Check if Internet is available
    
    Returns:
        True if Internet is available, False otherwise
    """
    check_urls = [
        settings.internet_check_url,  # Primary (configurable)
        "https://cloudflare.com",      # Fallback 1
        "https://github.com"           # Fallback 2
    ]
    
    for url in check_urls:
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.head(url)
                if response.status_code == 200:
                    return True
        except:
            continue
    
    return False
```

---

## 🔄 Mode Switching Logic

### LLM Client Selection

**When Internet Available (auto mode):**
1. Check connectivity status
2. If available → Use online LLM service (e.g., OpenAI, Anthropic, Gemini)
3. If unavailable → Fall back to local Ollama LLM

**When Internet Unavailable (auto mode):**
1. Check connectivity status
2. If unavailable → Use local Ollama LLM
3. Periodically check connectivity (every 30 seconds)
4. When connectivity restored → Switch back to online service

**Mode Switching Flow:**
```
User Request
    ↓
Check Connection Mode (auto/local/online)
    ↓
If auto:
    ↓
    Check Internet Connectivity
    ↓
    ├─ Internet Available?
    │   ├─ Yes → Use Online LLM Service
    │   └─ No → Use Local Ollama LLM
    │
    └─ Online Service Available?
        ├─ Yes → Process with Online Service
        └─ No → Fallback to Local Ollama LLM
    ↓
Response Generated
    ↓
Update Connectivity Status Cache
```

---

## ⚙️ Configuration

### Settings to Add

```python
# Connection Mode
connection_mode: str = Field(
    default="auto",
    description="Connection mode: auto (smart hybrid), local (offline-only), online (online-only)"
)

# Internet Detection
internet_check_url: str = Field(
    default="https://www.google.com",
    description="URL to check Internet connectivity"
)

internet_check_interval: int = Field(
    default=30,
    description="Internet connectivity check interval in seconds"
)

# Online LLM Service (when Internet available)
online_llm_provider: str = Field(
    default="openai",  # openai, anthropic, gemini
    description="Online LLM provider when Internet available"
)

online_llm_api_key: Optional[str] = Field(
    default=None,
    description="API key for online LLM service"
)

online_llm_model: str = Field(
    default="gpt-4",
    description="Online LLM model name"
)

# Fallback Behavior
fallback_to_local_on_error: bool = Field(
    default=True,
    description="Fallback to local LLM if online service fails"
)
```

---

## 🔧 Implementation Components

### 1. Connectivity Monitor (`src/utils/connectivity.py`)

**Purpose:** Monitor Internet connectivity status

**Key Functions:**
```python
async def check_internet_connectivity() -> bool:
    """Check if Internet is available"""

async def start_connectivity_monitor(interval: int = 30):
    """Start periodic connectivity monitoring"""

def get_connectivity_status() -> bool:
    """Get cached connectivity status"""
```

---

### 2. Enhanced LLM Client (`src/ai/llm_client.py`)

**Purpose:** Support both online and local LLM with automatic switching

**Key Changes:**
```python
class LLMClient:
    """Hybrid LLM client - auto-switches between online and local"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connection_mode = settings.connection_mode
        self.online_client = None  # Online LLM client
        self.local_client = None   # Local Ollama client
        self.connectivity_monitor = ConnectivityMonitor(settings)
    
    async def generate(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Generate response using appropriate LLM based on connectivity"""
        
        # Check connection mode
        if self.connection_mode == "local":
            return await self._generate_local(user_input, context)
        
        elif self.connection_mode == "online":
            return await self._generate_online(user_input, context)
        
        else:  # auto mode
            # Check connectivity
            if self.connectivity_monitor.is_online():
                try:
                    return await self._generate_online(user_input, context)
                except Exception as e:
                    logger.warning(f"Online LLM failed: {e}, falling back to local")
                    return await self._generate_local(user_input, context)
            else:
                return await self._generate_local(user_input, context)
    
    async def _generate_local(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Generate using local Ollama LLM"""
        # Existing local LLM logic
    
    async def _generate_online(self, user_input: str, context: Optional[Dict] = None) -> str:
        """Generate using online LLM service"""
        # New online LLM logic
```

---

### 3. Connection Mode Manager (`src/core/connection_manager.py`)

**Purpose:** Centralized connection mode management

**Key Functions:**
```python
class ConnectionManager:
    """Manage connection modes and connectivity detection"""
    
    async def get_current_mode() -> str:
        """Get current effective connection mode"""
    
    async def should_use_online() -> bool:
        """Determine if online services should be used"""
    
    async def switch_mode(new_mode: str):
        """Switch connection mode"""
```

---

## 📊 Status Tracking

### Dashboard Display

**Connection Status Indicator:**
- 🟢 Online - Using online services
- 🟡 Offline - Using local LLM (fallback)
- 🔵 Auto - Monitoring connectivity

**Real-time Status:**
- Current mode: `auto` / `local` / `online`
- Connectivity status: `Online` / `Offline`
- Active LLM: `Online Service` / `Local Ollama`
- Last connectivity check: `2025-11-03 09:15:30`

---

## 🔒 Privacy Considerations

### Data Handling

**Online Mode:**
- User queries may be sent to online services
- Response data may be processed by third-party services
- Configure privacy settings per user preference

**Local Mode:**
- 100% privacy - all data stays local
- No external API calls
- Complete data isolation

**Hybrid Mode (auto):**
- Uses online when available (better accuracy)
- Falls back to local when offline (privacy)
- User can configure to prefer local mode

---

## 🧪 Testing Strategy

### Unit Tests

1. **Connectivity Detection:**
   - Test Internet check with various endpoints
   - Test timeout handling
   - Test fallback logic

2. **Mode Switching:**
   - Test auto mode with Internet available
   - Test auto mode with Internet unavailable
   - Test manual mode switching

3. **LLM Client:**
   - Test online LLM generation
   - Test local LLM generation
   - Test fallback from online to local

### Integration Tests

1. **End-to-End Flow:**
   - Test complete request flow with auto mode
   - Test connectivity change during operation
   - Test error handling and fallback

---

## 📝 Implementation Checklist

### Phase 1: Connectivity Detection
- [ ] Create `src/utils/connectivity.py`
- [ ] Implement Internet connectivity check
- [ ] Implement periodic monitoring
- [ ] Add connectivity status caching

### Phase 2: Configuration
- [ ] Add connection mode settings to `settings.py`
- [ ] Add Internet check configuration
- [ ] Add online LLM service configuration
- [ ] Update `.env.example`

### Phase 3: LLM Client Enhancement
- [ ] Update `LLMClient` to support hybrid mode
- [ ] Implement online LLM client integration
- [ ] Implement automatic mode switching
- [ ] Add fallback logic

### Phase 4: Connection Manager
- [ ] Create `src/core/connection_manager.py`
- [ ] Implement centralized mode management
- [ ] Add mode switching API
- [ ] Integrate with orchestrator

### Phase 5: Dashboard Integration
- [ ] Add connectivity status display
- [ ] Add mode switching UI
- [ ] Add real-time status updates
- [ ] Add connection mode configuration

### Phase 6: Testing & Documentation
- [ ] Write unit tests
- [ ] Write integration tests
- [ ] Update documentation
- [ ] Update README.md

---

## 🚀 Future Enhancements

### Advanced Features

1. **Intelligent Mode Selection:**
   - Analyze query type to determine best mode
   - Some queries benefit from online (real-time data)
   - Some queries work fine locally (general knowledge)

2. **Connection Quality Detection:**
   - Monitor connection speed
   - Use online only if connection is stable
   - Fallback faster if connection is unstable

3. **Cost Optimization:**
   - Track API usage costs
   - Prefer local for simple queries
   - Use online only when necessary

4. **User Preferences:**
   - Allow per-query mode selection
   - Remember user preferences
   - Configure privacy levels per query type

---

## 📚 References

- **Current Implementation:** `src/ai/llm_client.py` (local only)
- **Settings:** `src/config/settings.py`
- **Architecture:** `docs/architecture/ARCHITECTURE.md`
- **User Requirement:** Direct feedback from user

---

**Status:** Design Complete - Ready for Implementation  
**Next Step:** Implement connectivity detection in SETUP-004 or AI-002

