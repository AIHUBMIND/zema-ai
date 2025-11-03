# verify_hardware.py Documentation

## File Location
`scripts/verify_hardware.py`

## Purpose
Hardware verification script for Insta360 Link 2 camera. Tests camera detection, video capture, PTZ controls, autofocus, and gesture support before development begins.

## Why It Was Created
CRITICAL: Verify hardware works BEFORE starting development to catch hardware issues early. This script:
- Detects camera hardware before coding
- Tests video capture functionality
- Verifies PTZ (Pan-Tilt-Zoom) controls
- Checks autofocus capability
- Confirms gesture support
- Saves test frame for manual verification

## How It Works

### Function: `check_v4l2_available() -> bool`
**Purpose**: Check if v4l2-ctl utility is available (required for PTZ controls)
**Returns**: True if v4l2-ctl is installed

### Function: `check_camera_detection() -> Tuple[bool, Optional[str]]`
**Purpose**: Detect Insta360 Link 2 camera
**How it works**:
1. Searches `/dev/video*` devices
2. Checks device capabilities using v4l2-ctl
3. Identifies Insta360 Link 2 by device name or capabilities
4. Returns device path if found

**Returns**: Tuple of (success, device_path)

### Function: `test_video_capture(device_path: str) -> bool`
**Purpose**: Test video capture functionality
**How it works**:
1. Opens camera using OpenCV (`cv2.VideoCapture`)
2. Captures test frame
3. Verifies frame is valid (not empty)
4. Saves test frame to `data/test_frame.jpg`

**Returns**: True if capture successful

### Function: `test_ptz_controls(device_path: str) -> bool`
**Purpose**: Test Pan-Tilt-Zoom controls
**How it works**:
1. Uses v4l2-ctl to send PTZ commands
2. Tests pan (horizontal movement)
3. Tests tilt (vertical movement)
4. Tests zoom (if available)
5. Verifies camera responds to commands

**Returns**: True if PTZ controls work

### Function: `check_autofocus(device_path: str) -> bool`
**Purpose**: Check autofocus capability
**How it works**:
1. Queries v4l2-ctl for autofocus controls
2. Checks if autofocus is available
3. Tests autofocus trigger

**Returns**: True if autofocus available

### Function: `check_gesture_support(device_path: str) -> bool`
**Purpose**: Check gesture recognition support
**How it works**:
1. Insta360 Link 2 processes gestures on-device
2. Checks for gesture detection firmware
3. Verifies LED blink detection (gesture indicator)

**Returns**: True if gesture support available

### Main Execution Flow
1. **Step 1**: Camera detection
   - Searches for Insta360 Link 2
   - Reports device path or failure
2. **Step 2**: Video capture test
   - Opens camera
   - Captures test frame
   - Saves frame to `data/test_frame.jpg`
3. **Step 3**: PTZ controls test
   - Tests pan, tilt, zoom
   - Verifies camera responds
4. **Step 4**: Autofocus test
   - Checks autofocus availability
   - Tests autofocus trigger
5. **Step 5**: Gesture support check
   - Verifies gesture detection firmware
   - Confirms LED blink detection

## Dependencies
- `opencv-python-headless`: Camera capture (`cv2`)
- `v4l-utils`: PTZ controls (`v4l2-ctl` command)
- `subprocess`: Running shell commands
- `pathlib`: File path handling

## Usage

### Basic Usage
```bash
python scripts/verify_hardware.py
```

### Expected Output
```
============================================================
ZEMA AI - Hardware Verification: Insta360 Link 2
============================================================

Step 1: Checking camera detection...
[OK] Camera detected: /dev/video0

Step 2: Testing video capture...
[OK] Video capture successful
[OK] Test frame saved: data/test_frame.jpg

Step 3: Testing PTZ controls...
[OK] PTZ controls working

Step 4: Testing autofocus...
[OK] Autofocus available

Step 5: Checking gesture support...
[OK] Gesture support available

VERIFICATION SUMMARY
[OK] All checks passed
```

### Exit Codes
- `0`: All tests passed
- `1`: Camera detection failed
- `2`: Video capture failed
- `3`: PTZ controls failed
- `4`: Other errors

## Error Handling

### Docker/Windows Environments
Script gracefully handles:
- Missing `v4l2-ctl` utility (skips PTZ tests)
- Missing OpenCV (skips video capture)
- Camera not found (provides troubleshooting steps)
- Permission errors (suggests running with sudo)

### Error Messages
- Clear warnings for missing dependencies
- Troubleshooting suggestions
- Environment-specific notes (Docker/Windows)

## Integration
- **Phase 0.5**: Hardware Verification (HARDWARE-001)
- **Before Development**: Run before starting Phase 1
- **Setup Scripts**: Can be called from setup automation
- **CI/CD**: Can be integrated into build pipeline

## Output Files
- `data/test_frame.jpg`: Test frame captured from camera
  - Used for manual verification
  - Shows camera is working correctly

## Benefits
1. **Early Detection**: Catch hardware issues before coding
2. **Clear Status**: Pass/fail for each test
3. **Test Evidence**: Saves test frame for verification
4. **Cross-Platform**: Works in Docker/Windows with graceful fallbacks
5. **Clear Output**: ASCII-compatible output (no emojis)

## Configuration
Script uses settings from `src/config/settings.py`:
- `camera_device_path`: Override camera device path
- `camera_device`: Camera device index (default: 0)

## Testing
```bash
# Run verification
python scripts/verify_hardware.py

# Check exit code
echo $?  # Should be 0 if successful

# Verify test frame
ls -lh data/test_frame.jpg
```

## Troubleshooting

### Camera Not Detected
1. Check camera is connected: `lsusb | grep Insta360`
2. Check device permissions: `ls -l /dev/video*`
3. Try running with sudo: `sudo python scripts/verify_hardware.py`
4. Check camera device path in settings

### PTZ Controls Not Working
1. Install v4l-utils: `sudo apt-get install v4l-utils`
2. Check device supports PTZ: `v4l2-ctl --list-ctrls`
3. Test manually: `v4l2-ctl --set-ctrl=pan_absolute=100`

### Video Capture Failed
1. Install OpenCV: `pip install opencv-python-headless`
2. Check camera permissions
3. Verify camera is not in use by another application

## Phase 0.5 Context
This script is part of **HARDWARE-001: Camera Detection & PTZ Test** in Phase 0.5 Hardware Verification. It must pass before proceeding to Phase 1 Voice Interaction.

