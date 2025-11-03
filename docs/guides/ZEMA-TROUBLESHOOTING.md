# ZEMA - Troubleshooting Guide
## Complete Problem Resolution for Raspberry Pi 5 + Insta360 Link 2

**For:** Zema AI Personal Assistant  
**Platform:** Raspberry Pi 5 (8GB) + Insta360 Link 2  
**Last Updated:** November 1, 2025

---

## Table of Contents

1. [Quick Diagnostics](#quick-diagnostics)
2. [Camera Issues](#camera-issues)
3. [Audio Problems](#audio-problems)
4. [AI/LLM Issues](#ai-llm-issues)
5. [Performance Problems](#performance-problems)
6. [Network & Dashboard](#network-dashboard)
7. [Voice Recognition](#voice-recognition)
8. [System Crashes](#system-crashes)
9. [Data & Storage](#data-storage)
10. [Advanced Debugging](#advanced-debugging)

---

## Quick Diagnostics

### Run Full System Check

```bash
# Quick health check script
python scripts/verify_hardware.py
python scripts/verify_audio.py
python scripts/verify_ollama.py

# Check Zema service status
sudo systemctl status zema

# Check logs for errors
tail -100 data/logs/zema.log | grep ERROR
```

### Common Symptoms & Quick Fixes

| Symptom | Likely Cause | Quick Fix |
|---------|--------------|-----------|
| "Camera not detected" | USB connection | Replug camera, try different port |
| "Ollama connection failed" | Service not running | `sudo systemctl start ollama` |
| Slow responses | High CPU usage | Restart Zema, check temperature |
| No wake word detection | Mic not working | Check audio device, test recording |
| Dashboard won't load | Port in use | Change port in .env |
| "Model not found" | Not downloaded | Run `bash scripts/download_models.sh` |

---

## Camera Issues

### Problem: Camera Not Detected

**Symptoms:**
- Error: "Insta360 Link 2 not found"
- `/dev/video0` doesn't exist
- `v4l2-ctl --list-devices` doesn't show camera

**Diagnosis:**
```bash
# Check USB devices
lsusb | grep -i insta360
# Should show: "Arashi Vision Insta360 Link 2"

# Check video devices
ls -l /dev/video*
# Should show at least /dev/video0

# Check dmesg for USB errors
dmesg | tail -20 | grep -i usb
```

**Solutions:**

**1. Basic reconnection:**
```bash
# Unplug camera USB
# Wait 5 seconds
# Plug back in
# Wait 10 seconds for detection

# Verify
v4l2-ctl --list-devices
```

**2. Try different USB port:**
- Camera needs USB 3.0 (blue port) for 4K
- Try all USB ports on Pi 5
- Avoid USB hubs (use direct connection)

**3. Power issue:**
```bash
# Check if Pi has enough power
vcgencmd get_throttled
# Output should be: throttled=0x0

# If throttled, camera may not get enough power
# Solution: Use official 27W power supply
```

**4. Kernel module issue:**
```bash
# Reload UVC driver
sudo modprobe -r uvcvideo
sudo modprobe uvcvideo

# Check module loaded
lsmod | grep uvcvideo
```

**5. Permissions:**
```bash
# Add user to video group
sudo usermod -a -G video $USER

# Logout and login again
# Or reboot
```

---

### Problem: Poor Video Quality

**Symptoms:**
- Blurry or pixelated video
- Low resolution despite settings
- Choppy video

**Diagnosis:**
```bash
# Check current settings
v4l2-ctl -d /dev/video0 --all | grep -E "(Width|Height|Format|FPS)"

# Test capture
ffmpeg -f v4l2 -i /dev/video0 -frames 1 test.jpg
# Check test.jpg quality
```

**Solutions:**

**1. Set correct format:**
```bash
# Force 1080p MJPEG @ 30fps
v4l2-ctl -d /dev/video0 \
  --set-fmt-video=width=1920,height=1080,pixelformat=MJPG
v4l2-ctl -d /dev/video0 --set-parm=30
```

**2. Enable Phase Detect AF:**
```bash
# Enable continuous autofocus
v4l2-ctl -d /dev/video0 --set-ctrl=focus_automatic_continuous=1
```

**3. Lighting check:**
- Link 2 needs minimum light level
- Even with f/1.8, complete darkness won't work
- Test with room lights on

**4. Clean lens:**
- Gently clean with microfiber cloth
- Camera lens exposed when deployed

**5. Reset camera:**
```bash
# Power cycle (unplug/replug)
# Or reset to defaults
v4l2-ctl -d /dev/video0 --set-ctrl=restore_defaults=1
```

---

### Problem: PTZ Not Working

**Symptoms:**
- Pan/tilt commands ignored
- Camera doesn't follow movement
- AI tracking not working

**Diagnosis:**
```bash
# Check PTZ controls available
v4l2-ctl -d /dev/video0 --list-ctrls | grep -E "(pan|tilt)"

# Try manual control
v4l2-ctl -d /dev/video0 --set-ctrl=pan_absolute=1000
# Camera should move
```

**Solutions:**

**1. Verify camera is in UVC mode:**
- If in Insta360 app mode, PTZ may not work
- Unplug camera, replug, don't open Insta360 app

**2. Reset PTZ position:**
```bash
# Center pan/tilt
v4l2-ctl -d /dev/video0 --set-ctrl=pan_absolute=0
v4l2-ctl -d /dev/video0 --set-ctrl=tilt_absolute=0
```

**3. Check AI tracking in code:**
```python
# In src/vision/camera.py
# Ensure tracking is enabled
self.tracking_enabled = True
```

---

### Problem: Gesture Recognition Not Working

**Symptoms:**
- Wave doesn't activate Zema
- Gestures not detected
- No LED blink on camera

**Diagnosis:**
```bash
# Link 2 gestures are on-device
# Check if camera LED blinks when you wave

# Test in good lighting
# Test at correct distance (0.5m - 3m)
```

**Solutions:**

**1. Lighting and distance:**
- Ensure good lighting (face/hands visible)
- Distance: 0.5 - 3 meters from camera
- Face camera directly (not at angle)

**2. Check gesture is enabled in settings:**
```bash
# In .env
CAMERA_GESTURES=true

# Restart Zema
sudo systemctl restart zema
```

**3. Try different gestures:**
- **Wave:** Move hand left-right clearly
- **Thumbs up:** Hold steady for 1-2 seconds
- **Peace sign:** Two fingers clear and steady

**4. Camera firmware:**
- Link 2 gesture processing is firmware-based
- Ensure latest firmware (check Insta360 website)

---

## Audio Problems

### Problem: No Audio Input

**Symptoms:**
- "Microphone not found"
- Wake word never detected
- Voice commands not heard

**Diagnosis:**
```bash
# List audio devices
arecord -l

# Test recording
arecord -D hw:1,0 -f cd -d 5 test.wav
aplay test.wav
# Can you hear yourself?
```

**Solutions:**

**1. Check camera microphone:**
```bash
# Camera mic usually shows as card 1
arecord -l | grep -i insta360

# If found, set as default
cat > ~/.asoundrc << 'EOF'
pcm.!default {
    type hw
    card 1
    device 0
}
EOF
```

**2. Permissions:**
```bash
# Add user to audio group
sudo usermod -a -G audio $USER
# Logout/login or reboot
```

**3. ALSA configuration:**
```bash
# Check ALSA status
alsamixer
# Press F6 to select camera
# Ensure not muted, volume at 80%+
```

**4. Test with PyAudio:**
```python
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"{i}: {info['name']} - Inputs: {info['maxInputChannels']}")
```

---

### Problem: Poor Audio Quality

**Symptoms:**
- Distorted audio
- Excessive noise
- Clipping/crackling

**Diagnosis:**
```bash
# Record test
arecord -D hw:1,0 -f cd -d 10 test.wav

# Check levels
aplay -v test.wav
# Look for clipping warnings

# Check with Audacity or similar
```

**Solutions:**

**1. Reduce input gain:**
```bash
alsamixer
# Press F6, select camera
# Reduce capture level to 70-80%
```

**2. Position camera correctly:**
- 1-2 meters from speaker (you)
- Not pointing at speakers (feedback)
- AI noise canceling should help, but can't fix everything

**3. Check sample rate:**
```bash
# Zema uses 16kHz
# Verify in settings
cat .env | grep SAMPLE_RATE
# Should be 16000
```

**4. Disable unused audio devices:**
```bash
# If multiple devices causing issues
# Disable unwanted ones in ALSA config
```

---

## AI/LLM Issues

### Problem: "Ollama Connection Failed"

**Symptoms:**
- Error: "Cannot connect to Ollama server"
- Timeout when generating responses
- Zema hangs when processing query

**Diagnosis:**
```bash
# Check if Ollama is running
systemctl status ollama
# Should be "active (running)"

# Test Ollama directly
ollama list
# Should show llama3.2:3b

# Test generation
echo "Say hello" | ollama run llama3.2:3b
```

**Solutions:**

**1. Start Ollama service:**
```bash
sudo systemctl start ollama

# Enable auto-start
sudo systemctl enable ollama

# Check status
systemctl status ollama
```

**2. Check port 11434:**
```bash
# Ollama runs on port 11434
netstat -tuln | grep 11434
# Should show LISTEN

# If blocked by firewall
sudo ufw allow 11434/tcp
```

**3. Restart Ollama:**
```bash
sudo systemctl restart ollama

# Check logs
journalctl -u ollama -n 50
```

**4. Reinstall Ollama:**
```bash
# If corrupted
curl -fsSL https://ollama.com/install.sh | sh
```

---

### Problem: Slow AI Responses

**Symptoms:**
- Takes >10 seconds to respond
- CPU at 100%
- Pi gets very hot (>80°C)

**Diagnosis:**
```bash
# Check CPU usage
htop
# Look for ollama process at 400% (all 4 cores)

# Check temperature
vcgencmd measure_temp
# Should be <75°C under load

# Benchmark Ollama
time echo "Count to 10" | ollama run llama3.2:3b
```

**Solutions:**

**1. Use smaller model:**
```bash
# llama3.2:1b is faster
ollama pull llama3.2:1b

# Update .env
LLM_MODEL=llama3.2:1b

# Restart Zema
sudo systemctl restart zema
```

**2. Reduce max_tokens:**
```bash
# In .env
LLM_MAX_TOKENS=256  # Down from 512

# Shorter responses = faster generation
```

**3. Cooling:**
```bash
# Check temperature
vcgencmd measure_temp

# Solutions:
# - Add heatsink or fan to Pi 5
# - Improve airflow around case
# - Don't run in enclosed space
```

**4. Optimize prompt:**
```python
# In src/ai/system_prompts.py
# Shorter system prompt = faster responses
# Remove unnecessary context
```

---

### Problem: "Model Not Found"

**Symptoms:**
- Error: "llama3.2:3b not found"
- Whisper model missing
- YOLO model not loading

**Diagnosis:**
```bash
# Check Ollama models
ollama list

# Check other models
ls -lh data/models/
```

**Solutions:**

**1. Download missing models:**
```bash
# Ollama
ollama pull llama3.2:3b

# All other models
bash scripts/download_models.sh

# Verify
ls -lh data/models/
```

**2. Check disk space:**
```bash
df -h
# Need at least 10GB free for models

# Clean up if needed
# Delete old logs, temp files
```

---

## Performance Problems

### Problem: High CPU Usage

**Symptoms:**
- CPU constantly >80%
- Pi very hot
- System sluggish

**Diagnosis:**
```bash
# Check what's using CPU
htop
# Press F5 for tree view

# Check Zema specifically
ps aux | grep python
```

**Solutions:**

**1. Identify bottleneck:**
```bash
# Check each component
# Camera: Should be <10% (Link 2 on-device AI)
# Ollama: 400% during inference, 0% idle
# YOLO: 50-80% when detecting
# Whisper: 100-200% during transcription
```

**2. Optimize settings:**
```bash
# In .env

# Reduce camera resolution
CAMERA_WIDTH=1280
CAMERA_HEIGHT=720  # Down from 1080p

# Use smaller models
LLM_MODEL=llama3.2:1b
STT_MODEL=tiny  # Down from base

# Reduce detection frequency
VISION_CONFIDENCE=0.6  # Higher = fewer false positives
```

**3. Disable unused features:**
```bash
# If don't need vision
FEATURE_VISION=false

# If don't need Ethiopian features
FEATURE_ETHIOPIAN=false
```

---

### Problem: High Memory Usage

**Symptoms:**
- RAM >7GB used
- System swapping to disk
- Out of memory errors

**Diagnosis:**
```bash
# Check memory
free -h

# Check what's using it
ps aux --sort=-%mem | head -10

# Check Zema
ps aux | grep python | awk '{print $11, $6}'
```

**Solutions:**

**1. Restart Zema:**
```bash
# Memory leaks over time are possible
sudo systemctl restart zema
```

**2. Reduce memory usage:**
```bash
# Use smaller models (see above)

# Reduce conversation history
# In src/core/orchestrator.py
# Keep only last 5 turns instead of 10
```

**3. Clear caches:**
```python
# In Python code, periodically:
import gc
gc.collect()
```

---

### Problem: System Overheating

**Symptoms:**
- vcgencmd measure_temp >80°C
- Throttling warnings
- System slows down

**Diagnosis:**
```bash
# Check temperature
watch -n 1 vcgencmd measure_temp

# Check throttling
vcgencmd get_throttled
# 0x0 = no throttling (good)
# Other = throttled (bad)
```

**Solutions:**

**1. Physical cooling:**
- Add official Pi 5 active cooler
- Improve case ventilation
- Point fan at Pi
- Don't stack devices

**2. Software:**
```bash
# Reduce maximum frequency (if desperate)
sudo raspi-config
# Performance Options → Overclock → None

# This will slow everything down but reduce heat
```

---

## Network & Dashboard

### Problem: Dashboard Won't Load

**Symptoms:**
- Can't access `http://zema.local:8000`
- Connection timeout
- "This site can't be reached"

**Diagnosis:**
```bash
# Check if dashboard is running
sudo systemctl status zema
# Should show "Dashboard available at http://..."

# Check port
netstat -tuln | grep 8000

# Check from Pi itself
curl http://localhost:8000
```

**Solutions:**

**1. Check firewall:**
```bash
# Allow port 8000
sudo ufw allow 8000/tcp

# Or disable firewall temporarily
sudo ufw disable
```

**2. Change hostname resolution:**
```bash
# If zema.local doesn't work, use IP address
hostname -I
# Use first IP: http://192.168.1.XXX:8000
```

**3. Restart dashboard:**
```bash
sudo systemctl restart zema

# Or change port in .env
DASHBOARD_PORT=8080
```

**4. Check browser:**
- Try different browser
- Clear cache
- Disable VPN
- Try from phone on same network

---

## Voice Recognition

### Problem: Wake Word Not Detected

**Symptoms:**
- Saying "Hey Zema" does nothing
- No response to wake word
- Log shows "Listening..." but never activates

**Diagnosis:**
```bash
# Check logs
tail -f data/logs/zema.log | grep -i wake

# Test microphone (see audio section above)
```

**Solutions:**

**1. Increase sensitivity:**
```bash
# In .env
WAKEWORD_SENSITIVITY=0.7  # Up from 0.5

# Restart
sudo systemctl restart zema
```

**2. Speak clearly:**
- Louder than normal speaking
- Clear pronunciation: "HEY ZEE-MA"
- Face camera/microphone
- Not too fast or slow

**3. Check Porcupine:**
```bash
# May need API key for Porcupine
# Alternative: Use openwakeword (open-source)
pip install openwakeword
```

**4. Try different wake word:**
```bash
# In .env
WAKEWORD_KEYWORDS=zema  # Just "zema", not "hey zema"
```

---

### Problem: Speech Not Transcribed

**Symptoms:**
- Wake word works
- Zema chimes
- But never responds to speech
- Logs show "Listening..." then timeout

**Diagnosis:**
```bash
# Check Whisper logs
tail -f data/logs/zema.log | grep -i whisper

# Test Whisper directly
# Record 5 seconds
arecord -D hw:1,0 -f S16_LE -r 16000 -c 1 -d 5 test.wav

# Transcribe with faster-whisper
python << 'EOF'
from faster_whisper import WhisperModel
model = WhisperModel("base")
segments, info = model.transcribe("test.wav")
for segment in segments:
    print(segment.text)
EOF
```

**Solutions:**

**1. Check VAD settings:**
```bash
# In .env
# Voice Activity Detection may be too strict
# Adjust in src/voice/vad.py:
# aggressiveness = 1  # Down from 2
# silence_threshold = 600  # Down from 900ms
```

**2. Audio quality:**
- Speak louder
- Reduce background noise
- Speak closer to camera (1-2m)

**3. Use smaller/different model:**
```bash
# Try tiny model (faster, may help)
STT_MODEL=tiny
```

---

## System Crashes

### Problem: Zema Keeps Crashing

**Symptoms:**
- Service stops frequently
- systemctl shows "failed"
- Logs show exceptions

**Diagnosis:**
```bash
# Check crash logs
journalctl -u zema -n 100 --no-pager | grep -i error

# Check Python errors
tail -100 data/logs/zema.log | grep -i exception
```

**Solutions:**

**1. Fix the bug:**
- Read error message
- Fix in code
- Restart

**2. Enable auto-restart:**
```bash
# Edit service file
sudo nano /etc/systemd/system/zema.service

# Ensure these lines:
Restart=always
RestartSec=10

# Reload
sudo systemctl daemon-reload
sudo systemctl restart zema
```

**3. Add error handling:**
```python
# Wrap main loop in try/except
try:
    await orchestrator.start()
except Exception as e:
    logger.error(f"Fatal error: {e}")
    # Auto-restart via systemd
```

---

## Data & Storage

### Problem: "Disk Full"

**Symptoms:**
- Errors writing files
- Can't save conversations
- Models won't download

**Diagnosis:**
```bash
# Check disk space
df -h
# Look at / partition

# Find large files
du -sh data/* | sort -h
```

**Solutions:**

**1. Clean up:**
```bash
# Clear old logs
find data/logs/ -name "*.log.*" -mtime +7 -delete

# Clear old conversations (backup first!)
# python scripts/backup.sh
# rm data/db/conversations.db

# Clear temp files
rm -rf /tmp/*
```

**2. Move to USB storage:**
```bash
# Move data directory to USB drive
sudo mv data /mnt/usb/zema-data
sudo ln -s /mnt/usb/zema-data data
```

---

## Advanced Debugging

### Enable Verbose Logging

```bash
# In .env
LOG_LEVEL=DEBUG

# Restart
sudo systemctl restart zema

# Watch logs
tail -f data/logs/zema.log
```

### Run Zema in Foreground

```bash
# Stop service
sudo systemctl stop zema

# Activate venv
source venv/bin/activate

# Run directly (see all output)
python src/main.py

# Ctrl+C to stop
```

### Debug with Python Debugger

```python
# Add to code where needed
import pdb; pdb.set_trace()

# Or use ipdb for better experience
import ipdb; ipdb.set_trace()
```

### Monitor Resource Usage

```bash
# Watch CPU, memory, temperature
watch -n 2 '
echo "=== CPU ==="
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk "{print 100 - \$1\"%\"}"
echo ""
echo "=== Memory ==="
free -h | grep Mem
echo ""
echo "=== Temp ==="
vcgencmd measure_temp
echo ""
echo "=== Zema Process ==="
ps aux | grep python | grep -v grep
'
```

---

## Still Having Issues?

### Collect Debug Information

```bash
# Run diagnostics
python scripts/verify_hardware.py > debug_hardware.txt 2>&1
python scripts/verify_audio.py > debug_audio.txt 2>&1
python scripts/verify_ollama.py > debug_ollama.txt 2>&1

# Collect logs
tar -czf zema-debug.tar.gz \
    data/logs/ \
    debug_*.txt \
    .env

# Review zema-debug.tar.gz
```

### Check Common Mistakes

- [ ] Camera USB connection secure?
- [ ] Using official 27W power supply?
- [ ] All models downloaded?
- [ ] Ollama service running?
- [ ] Correct .env settings?
- [ ] Pi OS up to date?
- [ ] Enough disk space (>10GB)?
- [ ] Proper ventilation/cooling?

### Get Help

If none of these solutions work, you may have found a bug or edge case. Document:
1. Exact error message
2. Steps to reproduce
3. System info (`uname -a`, `python --version`)
4. Hardware setup
5. Debug files

---

## Prevention

### Regular Maintenance

```bash
# Weekly
sudo systemctl restart zema  # Fresh start
bash scripts/backup.sh        # Backup data

# Monthly
sudo apt update && sudo apt upgrade -y
bash scripts/cleanup.sh       # Clear old files
python scripts/benchmark.py   # Check performance
```

### Monitoring

```bash
# Add to cron for daily checks
0 2 * * * /home/pi/zema-ai/scripts/verify_hardware.py
0 3 * * * /home/pi/zema-ai/scripts/backup.sh
```

---

**Remember:** Most issues are simple - camera unplugged, service not running, wrong settings. Start with the basics!

🎉 **Happy troubleshooting!**