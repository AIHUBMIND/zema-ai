# Voice Module Documentation

## Purpose
The `src/voice/` folder handles all voice-related functionality: audio input/output, wake word detection, speech-to-text, text-to-speech, and voice activity detection.

## Files in This Folder

### `audio_io.py`
Audio input/output manager. Handles microphone input and speaker output using PyAudio. Manages audio devices, streams, and async recording/playback.

### `wakeword.py`
Wake word detection ("Hey Zema"). Listens for wake word to activate the assistant.

### `stt.py` (Speech-to-Text)
Converts speech audio to text using Faster Whisper. Supports multiple languages (English, Amharic).

### `tts.py` (Text-to-Speech)
Converts text to speech using Piper TTS. Supports multiple voices and configurable speed.

### `vad.py` (Voice Activity Detection)
Detects when user is speaking vs silence. Uses WebRTC VAD library to identify speech segments.

## Audio Flow
```
Microphone → AudioIO → VAD → STT → Text
                                          ↓
Text → TTS → AudioIO → Speaker
```

## Key Features
- Async audio I/O
- Multiple language support
- Device detection and selection
- Voice activity detection
- Wake word activation

