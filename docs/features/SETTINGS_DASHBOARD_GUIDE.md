# Settings Dashboard - Categorization Guide

## ✅ Settings to ADD to Dashboard (User-Facing)

These settings should be exposed in the dashboard because users need to configure them:

### 🔒 Privacy & Security
- **Privacy Mode** (local/hybrid/cloud) - Users control data privacy
- **Data Retention Days** - Users control how long data is kept

### 🎤 Voice & Audio
- **Wake Word Keywords** - Users customize activation phrase
- **Wake Word Sensitivity** - Users adjust sensitivity (slider 0.0-1.0)
- **STT Language** - Users select language (English/Amharic/Auto)
- **TTS Voice** - Users choose voice (dropdown with preview)
- **TTS Speed** - Users adjust speaking speed (slider 0.5-2.0)

### 📹 Camera & Vision
- **Camera Tracking** - Users toggle AI tracking (on/off)
- **Camera Gestures** - Users toggle gesture recognition (on/off)

### 🤖 AI & Intelligence
- **LLM Model** - Users select AI model (dropdown with model info)
- **LLM Temperature** - Users adjust creativity (slider 0.0-2.0)
- **LLM Max Tokens** - Users control response length (number input)

### 🎯 Features
- **Feature Voice** - Users enable/disable voice features
- **Feature Vision** - Users enable/disable vision features
- **Feature Tasks** - Users enable/disable task management
- **Feature Ethiopian** - Users enable/disable Ethiopian features

### 🔑 API Keys (Optional)
- **Gemini API Key** - Users add optional API keys
- **ElevenLabs API Key** - Users add optional API keys

### 📊 System
- **Log Level** - Users adjust logging verbosity (for debugging)

---

## ❌ Settings NOT to Add to Dashboard (Technical/Advanced)

These settings should NOT be exposed in the dashboard because:
- They're technical/internal
- Users shouldn't need to change them
- Auto-detected/managed by system
- Developer-only settings

### 🚫 Technical Settings (Keep in .env only)
- `environment` - Set at deployment
- `hostname` - Set at deployment
- `dashboard_port` - Set at deployment
- `dashboard_host` - Set at deployment
- `database_url` - Technical, auto-managed
- `enable_dashboard` - Contradictory if disabled

### 🚫 Hardware-Specific (Auto-Detected)
- `camera_device` - Auto-detected
- `camera_device_path` - Auto-detected
- `audio_device_name` - Auto-detected
- `audio_input_device_index` - Auto-detected
- `audio_output_device_index` - Auto-detected

### 🚫 Model Paths (Auto-Managed)
- `models_base_path` - System-managed
- `whisper_model_path` - System-managed
- `piper_model_path` - System-managed
- `yolo_model_path` - System-managed

### 🚫 Hardware Verification (Developer Settings)
- `hardware_verification_enabled` - Developer setting
- `hardware_verification_camera_test` - Developer setting
- `hardware_verification_audio_test` - Developer setting
- `hardware_verification_ollama_test` - Developer setting

### 🚫 Performance Thresholds (System Settings)
- `ollama_time_to_first_token_max_ms` - System threshold
- `ollama_tokens_per_second_min` - System threshold
- `ollama_memory_usage_max_gb` - System threshold
- `audio_latency_max_ms` - System threshold
- `camera_capture_fps_min` - System threshold

### 🚫 Ollama Connection (System Settings)
- `ollama_url` - Default localhost is fine
- `ollama_timeout` - System-managed
- `ollama_health_check_timeout` - System-managed

### 🚫 Technical Audio/Camera Settings
- `audio_sample_rate` - Standard (16000Hz)
- `audio_channels` - Standard (mono)
- `camera_width` - Camera-dependent
- `camera_height` - Camera-dependent
- `camera_fps` - Camera-dependent
- `stt_model` - Model-dependent
- `tts_engine` - Fixed (Piper)
- `vision_detection_model` - Model-dependent
- `vision_confidence_threshold` - Fine-tuned, not user-facing

---

## 📋 Recommended Dashboard Settings Layout

### Tab 1: General
- Privacy Mode
- Data Retention Days
- Log Level

### Tab 2: Voice & Audio
- Wake Word Keywords
- Wake Word Sensitivity
- STT Language
- TTS Voice (with preview)
- TTS Speed

### Tab 3: Camera & Vision
- Camera Tracking (toggle)
- Camera Gestures (toggle)

### Tab 4: AI & Intelligence
- LLM Model (dropdown)
- LLM Temperature (slider)
- LLM Max Tokens
- System Prompt (advanced, collapsible)

### Tab 5: Features
- Feature Voice (toggle)
- Feature Vision (toggle)
- Feature Tasks (toggle)
- Feature Ethiopian (toggle)

### Tab 6: API Keys
- Gemini API Key (optional)
- ElevenLabs API Key (optional)

---

## 🎯 Summary

**ADD to Dashboard:** ~20 user-facing settings
**KEEP in .env only:** ~25 technical/system settings

This provides a clean, user-friendly interface while keeping technical details hidden.
