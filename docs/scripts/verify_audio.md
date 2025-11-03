# verify_audio.py Documentation

## File Location
`scripts/verify_audio.py`

## Purpose
Audio device verification script. Tests microphone and speaker functionality, measures audio quality, and verifies 16kHz capture works correctly for voice assistant requirements.

## Why It Was Created
Audio quality is critical for voice assistant functionality. This script:
- Lists all available audio devices
- Tests Insta360 Link 2 microphone
- Tests speaker output
- Measures audio quality (SNR, latency)
- Verifies 16kHz capture works
- Saves test recording for manual review

## How It Works

### Function: `list_audio_devices() -> Tuple[List[dict], List[dict]]`
**Purpose**: List all available audio input/output devices
**How it works**:
1. Uses PyAudio to enumerate devices
2. Identifies input devices (microphones)
3. Identifies output devices (speakers)
4. Shows device name, index, channels, sample rate

**Returns**: Tuple of (input_devices, output_devices)

### Function: `test_microphone_recording(device_index: Optional[int] = None) -> Tuple[bool, Optional[str]]`
**Purpose**: Test microphone recording
**How it works**:
1. Opens audio stream (16kHz, mono, 16-bit)
2. Records 5 seconds of audio
3. Saves to WAV file (`data/test_recording.wav`)
4. Verifies recording is not empty
5. Checks for clipping/distortion (if numpy available)

**Returns**: Tuple of (success, file_path)

### Function: `test_speaker_playback(file_path: str, device_index: Optional[int] = None) -> bool`
**Purpose**: Test speaker playback
**How it works**:
1. Loads test recording
2. Plays back through speaker
3. Measures playback latency
4. Verifies playback completes

**Returns**: True if playback successful

### Function: `verify_16khz_capture(device_index: Optional[int] = None) -> bool`
**Purpose**: Verify 16kHz capture works
**How it works**:
1. Records short sample at 16kHz
2. Verifies sample rate is correct
3. Checks audio quality

**Returns**: True if 16kHz capture works

### Main Execution Flow
1. **Step 1**: List audio devices
   - Shows all input devices
   - Shows all output devices
   - Displays device information
2. **Step 2**: Test microphone recording
   - Records 5 seconds
   - Saves to `data/test_recording.wav`
   - Verifies recording quality
3. **Step 3**: Test speaker playback
   - Plays back test recording
   - Measures latency
   - Verifies playback works
4. **Step 4**: Verify 16kHz capture
   - Tests 16kHz recording
   - Verifies sample rate
   - Confirms quality

## Dependencies
- `pyaudio`: Audio I/O
- `wave`: WAV file handling
- `numpy`: Audio quality analysis (optional)
- `scipy.io.wavfile`: WAV file reading (optional)

## Usage

### Basic Usage
```bash
python scripts/verify_audio.py
```

### Expected Output
```
============================================================
Step 1: Listing audio devices...
[OK] Found 2 input devices
[OK] Found 3 output devices

Step 2: Testing microphone recording...
[OK] Recording successful
[OK] Test recording saved: data/test_recording.wav

Step 3: Testing speaker playback...
[OK] Playback successful
[OK] Latency: 5.2ms

Step 4: Verifying 16kHz capture...
[OK] 16kHz capture working
[OK] Sample rate verified: 16000 Hz

VERIFICATION SUMMARY
[OK] All audio tests passed
```

### Exit Codes
- `0`: All audio tests passed
- `1`: Microphone failed
- `2`: Speaker failed
- `3`: Quality issues detected
- `4`: Other errors

## Error Handling

### Docker/Windows Environments
Script gracefully handles:
- Missing PyAudio (warns but continues)
- Missing numpy (skips quality analysis)
- No audio devices (provides troubleshooting)
- Permission errors (suggests running with sudo)

### Error Messages
- Clear warnings for missing dependencies
- Troubleshooting suggestions
- Device-specific errors

## Integration
- **Phase 0.5**: Hardware Verification (HARDWARE-002)
- **Before Development**: Run before starting Phase 1
- **Setup Scripts**: Can be called from setup automation
- **CI/CD**: Can be integrated into build pipeline

## Output Files
- `data/test_recording.wav`: Test audio recording
  - 5 seconds of microphone input
  - 16kHz, mono, 16-bit PCM
  - Used for manual verification

## Configuration
Script uses settings from `src/config/settings.py`:
- `audio_input_device_index`: Override input device index
- `audio_output_device_index`: Override output device index
- `audio_sample_rate`: Sample rate (default: 16000 Hz)
- `audio_channels`: Channels (default: 1 = mono)

## Benefits
1. **Device Discovery**: Lists all available audio devices
2. **Quality Verification**: Tests recording and playback quality
3. **Latency Measurement**: Measures audio latency
4. **16kHz Verification**: Ensures correct sample rate for Whisper
5. **Clear Output**: ASCII-compatible output (no emojis)
6. **Cross-Platform**: Works in Docker/Windows with graceful fallbacks

## Testing
```bash
# Run verification
python scripts/verify_audio.py

# Check exit code
echo $?  # Should be 0 if successful

# Listen to test recording
aplay data/test_recording.wav  # Linux
# or play on Windows/macOS
```

## Troubleshooting

### No Audio Devices Found
1. Check audio devices: `pactl list short sources` (Linux)
2. Check device permissions
3. Try running with sudo: `sudo python scripts/verify_audio.py`
4. Verify audio hardware is connected

### Microphone Recording Failed
1. Check microphone permissions
2. Verify microphone is not muted
3. Check device index in settings
4. Test manually: `arecord -d 5 test.wav` (Linux)

### Speaker Playback Failed
1. Check speaker permissions
2. Verify speaker is not muted
3. Check device index in settings
4. Test manually: `aplay data/test_recording.wav` (Linux)

### 16kHz Capture Not Working
1. Verify device supports 16kHz
2. Check sample rate settings
3. Verify PyAudio installation

## Phase 0.5 Context
This script is part of **HARDWARE-002: Audio Device Verification** in Phase 0.5 Hardware Verification. It must pass before proceeding to Phase 1 Voice Interaction.

