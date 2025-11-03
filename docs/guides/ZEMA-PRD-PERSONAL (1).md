# ZEMA AI Personal Assistant - Master Project Blueprint
## Complete Development Guide for Personal AI Assistant

**Project Status:** Design & Planning Phase  
**Target Platform:** Raspberry Pi 5 + Insta360 Link 2 Camera  
**Purpose:** Private, Personal AI Assistant (Single Owner, Family Access)  
**Last Updated:** November 1, 2025

---

## Table of Contents

1. [Product Vision](#product-vision)
2. [Core Principles](#core-principles)
3. [Key Features](#key-features)
4. [User Scenarios](#user-scenarios)
5. [Technical Stack](#technical-stack)
6. [Development Phases](#development-phases)
7. [Success Criteria](#success-criteria)

---

## 1. Product Vision

### What is Zema?

**Zema** ([translate:ዜማ] - meaning "melody" or "chant" in Amharic) is your **personal, portable, AI-powered assistant** that combines voice and vision capabilities to help with everyday tasks, problem-solving, creative work, and household management.

### Primary Use Case

- **Owner:** You (primary user with full control)
- **Secondary Users:** Family members (wife, kids) with appropriate access
- **Environment:** Home, office, or anywhere with power and optional Wi-Fi
- **Privacy:** 100% local processing by default, cloud features opt-in only

### Design Philosophy

> "Zema is not a product—it's a personal companion. Everything it knows, sees, and does is private to you and your family. It goes where you go, learns from you (not from the internet), and respects your privacy above all else."

### What Makes Zema Different

- **Truly Private:** All data stays on your device unless you explicitly opt-in
- **Portable:** Fits in a small case, runs on USB power, connects to any Wi-Fi
- **Multimodal:** Voice + Vision working together (not separate features)
- **Personal:** Learns YOUR preferences, YOUR schedule, YOUR family
- **Offline-Capable:** Core features work without internet
- **Family-Friendly:** Safe for kids, respects household context

---

## 2. Core Principles

### Privacy First
- **Local by Default:** All processing happens on Raspberry Pi
- **No Cloud Required:** Core features work 100% offline
- **Data Ownership:** You own all data, can delete anytime
- **No Tracking:** Never sends analytics or usage data anywhere
- **Opt-in Cloud:** Only use external APIs when you explicitly enable them

### Portability
- **Single Device:** Raspberry Pi 5 + Camera + Mic/Speaker in one package
- **Power Flexible:** USB-C power (laptop, battery pack, wall outlet)
- **Network Flexible:** Works on any Wi-Fi or fully offline
- **Easy Transport:** Take between home, office, travel

### Simplicity
- **Voice First:** Natural conversation, no complex commands
- **Visual Context:** Camera provides situational awareness
- **No Apps Needed:** Standalone system, optional web dashboard
- **Quick Setup:** 5 minutes from power-on to first conversation

### Extensibility
- **Modular Design:** Easy to add new features/skills
- **Open Architecture:** Based on standard Python, easy to customize
- **Future-Proof:** Ready for voice-driven programming era
- **Community Ready:** Could be open-sourced later if desired

---

## 3. Key Features

### Voice Interaction

**Wake Word Activation**
- "Hey Zema" or "[translate:ዜማ]"
- Always listening (privacy mode can disable)
- Multi-language support (English + Amharic)

**Natural Conversation**
- Context-aware (remembers previous questions)
- Interruption handling (can stop Zema mid-sentence)
- Code-switching (mix English and Amharic naturally)
- Personality customization (friendly, professional, casual)

**Speech Quality**
- Fast response (<2 seconds typical)
- Natural-sounding voice (not robotic)
- Volume auto-adjustment
- Background noise filtering (AI noise canceling dual mic)

### Vision Capabilities

**Scene Understanding**
- "What do you see?" - Describes surroundings
- Object identification and counting
- Text reading (OCR)
- Color and lighting detection
- Superior low-light performance (f/1.8 aperture)

**Measurement & Analysis**
- Measure object dimensions
- Distance estimation with calibrated focal length
- Compare sizes
- Detect changes in scene
- Minimal lens distortion for accurate measurements

**3D Modeling (Basic)**
- Generate simple 3D models from photos
- Export as STL/OBJ files
- Measurements for CAD work
- Reference for 3D printing

**Gesture Control** (Hardware-Accelerated)
- Wave to activate (without wake word) - **on-device AI chip**
- Thumbs up/down for confirmation
- Stop hand to pause
- Point to select objects
- **No CPU load on Pi** - gestures processed by camera's built-in AI

**Advanced Camera Features**
- **Motorized PTZ:** ±150° pan / ±45° tilt
- **AI Tracking:** Follows you automatically (on-device processing)
- **Phase Detect Autofocus:** Fast, accurate (0.2s)
- **HDR:** Better dynamic range in mixed lighting
- **65° HFOV:** Wide enough for room coverage, narrow enough for detail

### Personal Assistant Tasks

**Scheduling & Reminders**
- "Schedule a meeting tomorrow at 3pm"
- "Remind me to water plants at 5pm"
- "What's on my calendar today?"
- Recurring reminders

**Note Taking**
- "Take a note: buy milk"
- "What did I tell you last week about the project?"
- Voice memos saved and searchable
- Export notes to files

**Task Management**
- To-do lists
- Project tracking
- Progress monitoring
- Priority management

**Information & Research**
- General knowledge questions
- Web search (when online)
- Fact checking
- Quick translations

### Ethiopian Cultural Integration

**Language Support**
- Amharic speech recognition
- Amharic text-to-speech
- Code-switching (mix languages)
- Ethiopian English accent optimization

**Cultural Knowledge**
- Ethiopian Orthodox Church information
- Saints and feast days
- Fasting periods (Tsom)
- Liturgical music ([translate:ዜማ]) education

**Calendar & Time**
- Ethiopian calendar conversion (13 months)
- Ethiopian time system (starts at sunrise)
- Holiday notifications
- Cultural event reminders

**Recipes & Cooking**
- Traditional Ethiopian recipes
- Step-by-step cooking guidance
- Ingredient substitutions
- Vision-assisted cooking help (identify ingredients)

### Smart Home Integration (Optional)

**Basic Controls**
- Lights on/off, dimming
- Thermostat adjustment
- Media playback
- Device status checking

**Automation**
- Morning/evening routines
- Location-based actions
- Schedule-based automation
- Voice-triggered scenes

### Privacy & Security

**Privacy Modes**
- **Full Privacy:** Everything offline, no external APIs
- **Hybrid:** Simple tasks local, complex tasks cloud
- **Connected:** Full cloud features enabled

**Data Control**
- View all stored data
- Delete conversation history
- Export personal data
- Clear all data command

**Physical Indicators**
- **Built-in LED** shows when camera is active
- Visual privacy mode indicator
- Mute buttons for mic and camera

---

## 4. User Scenarios

### Scenario 1: Morning Routine at Home

```
You: "Hey Zema, good morning"
Zema: "Good morning! It's Saturday, November 2nd, 8:30 AM. You have 
       a dentist appointment at 2 PM. Would you like to hear the weather?"

You: "Yes please"
Zema: "It's 65°F and partly cloudy in Rockville. High of 70°F expected."

You: "Remind me to pick up groceries before the appointment"
Zema: "Got it. I'll remind you at 12:30 PM to pick up groceries 
       before your 2 PM dentist appointment."
```

### Scenario 2: Vision-Assisted Work (Office)

```
You: "Zema, take a picture of this component"
Zema: [Camera auto-focuses with phase detect AF, captures sharp 4K image]
      "Photo captured. What would you like me to do with it?"

You: "Can you measure it and create a simple 3D model?"
Zema: "Analyzing with calibrated focal length... This appears to be a 
       rectangular bracket, approximately 8 cm x 5 cm x 2 cm. 
       Generating 3D model..."
       [Processing with minimal lens distortion for accuracy]
       "Model complete. I've saved it as 'bracket_20251102.stl' 
       on your desktop. Would you like me to open it?"

You: "Yes, and send the measurements to my notes"
Zema: "Done. Opening model viewer and added measurements to 
       your project notes."
```

### Scenario 3: Gesture-Controlled Interaction

```
[You wave at camera while across the room]
Zema: [On-device AI chip detects gesture instantly, no Pi CPU load]
      "Hey! I see you waving. How can I help?"

You: "What do you see in front of me?"
Zema: [AI tracking follows you automatically as you move]
      "I see you standing at your workbench with a laptop, 
       coffee mug, and some electronic components. The lighting 
       is good thanks to the window on your right."

[You give thumbs up]
Zema: [Gesture recognized by camera's AI processor]
      "Great! Anything else you need?"
```

### Scenario 4: Cooking with Family

```
You: "Zema, what can I make with what you see?"
Zema: [PTZ camera tilts down to kitchen counter, HDR handles bright 
       window and shadowed ingredients]
      "I see onions, tomatoes, berbere spice, chicken, and oil. 
       You have everything for Doro Wat! Would you like the recipe?"

Wife: "Yes, start from the beginning"
Zema: [Recognizes different voice, AI tracking shifts to her]
      "Hi! Starting Doro Wat recipe. First, finely chop 3 large 
       onions. Let me know when you're ready for the next step."
       
[Later]
You: "Zema, how much longer?"
Zema: [Camera tracks back to you at stove]
      "The chicken should simmer for another 25 minutes. I'll 
       remind you when it's time to check it."
```

### Scenario 5: Low-Light Evening Use

```
[Evening, dim room lighting]

You: "Hey Zema, help me find my keys"
Zema: [f/1.8 aperture + HDR captures clear image even in low light]
      "Looking around... I can see your keys on the coffee table, 
       next to the TV remote."

You: "Where exactly?"
Zema: [Camera pans to focus on coffee table]
      "Right there - they're on the left side of the table, 
       partially under a magazine."
```

### Scenario 6: Portable Use (Office)

```
[At office, plug in Zema via USB to laptop, auto-connects to office Wi-Fi]

Zema: "Hello! I'm now connected to Office Network. Ready to assist."

You: "Zema, what meetings do I have today?"
Zema: "You have three meetings:
       - 10 AM: Team standup
       - 1 PM: Client presentation
       - 4 PM: Project review
       
       Would you like details on any of these?"

You: "Take notes during my 1 PM presentation"
Zema: [AI tracking will follow you during presentation]
      "I'll activate note-taking mode at 1 PM. I'll transcribe 
       the discussion and create a summary for you afterward."
```

---

## 5. Technical Stack

### Hardware

**Required Components**
- **Raspberry Pi 5** (8GB RAM) - $80
- **Insta360 Link 2** (4K PTZ AI Webcam) - $299
  - 1/2" CMOS sensor with Phase Detect AF + HDR
  - f/1.8 aperture (superior low-light performance)
  - ±150° pan / ±45° tilt motorized AI tracking
  - Built-in AI chip for gesture recognition (no Pi CPU load)
  - AI noise canceling dual microphones
  - UVC compliant (plug-and-play Linux support)
  - 65° HFOV with minimal distortion
  - USB-C, 5V/1A (~5W power draw)
- **USB-C Power Supply** (27W official) - $12
- **MicroSD Card** (64GB+, UHS-I) - $15
- **USB Speaker** or use 3.5mm audio output - $20-50
- **Raspberry Pi 5 Case** with active cooling - $15
- **Optional:** USB battery pack for portability - $40-80

**Total Hardware Cost:** ~$441-521 (camera upgrade justified by on-device AI)

### Camera Selection Rationale

**Why Insta360 Link 2 over OBSBOT Tiny 2 Lite:**

| Feature | Insta360 Link 2 | OBSBOT Tiny 2 Lite |
|---------|----------------|-------------------|
| **Sensor Quality** | 1/2" CMOS (larger) | 1/2.8" CMOS (smaller) |
| **Autofocus** | Phase Detect (fast, accurate) | Contrast AF (slower) |
| **On-device AI** | Yes (gesture + tracking) | Software-dependent |
| **Linux Support** | UVC plug-and-play | Requires OBSBOT Center app |
| **CPU Load** | Zero (on-board AI chip) | High (Pi processes tracking) |
| **Lens Quality** | f/1.8, minimal distortion | f/1.9, more distortion |
| **Power** | 5W (efficient) | 7.5W |
| **Thermal** | Excellent (stays cool) | Moderate heat |
| **Firmware** | Very stable | Occasional crashes |
| **Privacy** | All on-device | Some cloud calls |
| **Cost** | $299 | $159 |

**Decision:** Insta360 Link 2's on-device AI processing, superior sensor, and zero Pi CPU overhead make it ideal for edge AI applications. The $140 premium is justified by:
- No CPU load for gesture recognition (critical for Pi 5)
- Better image quality for OpenCV + YOLO detection
- Stable Linux UVC support (no vendor software needed)
- More accurate measurements (calibrated lens)
- True offline privacy (no cloud dependencies)

### Software Stack

**Operating System**
- Raspberry Pi OS Lite (64-bit, Debian-based)
- Custom auto-start scripts
- Systemd services for Zema

**Programming Language**
- Python 3.11+
- Type hints throughout
- Async/await architecture
- Poetry for dependency management

**AI & ML**
- **LLM:** Ollama + Llama 3.2-3B (local inference)
- **STT:** Whisper.cpp (local speech recognition)
- **TTS:** Piper TTS (local voice synthesis) or ElevenLabs (cloud, optional)
- **Vision:** OpenCV + YOLOv8-nano (object detection)

**Data Storage**
- SQLite (lightweight, local database)
- File-based storage for media
- JSON for configuration

**Optional Cloud Services** (Opt-in)
- Google Gemini (advanced AI)
- ElevenLabs (premium voice)
- Web search APIs

### Key Python Libraries

```python
# Core AI & ML
ollama-python          # Local LLM inference
whisper-cpp-python     # Fast STT
piper-tts             # Local TTS
opencv-python         # Computer vision
ultralytics           # YOLOv8 for object detection

# Audio Processing
pyaudio               # Audio I/O (uses camera's AI noise canceling mic)
webrtcvad            # Voice activity detection
pvporcupine          # Wake word detection

# Camera Integration
v4l2-ctl             # Video4Linux camera control
uvc                  # USB Video Class interface

# Web & API
fastapi              # Optional web dashboard
httpx                # HTTP client
python-dotenv        # Environment configuration

# Data & Storage
aiosqlite            # Async SQLite
pydantic             # Data validation

# Utilities
python-dateutil      # Date/time parsing
pillow               # Image processing
numpy                # Numerical operations
```

---

## 6. Development Phases

### Phase 0: Setup (Week 1)
**Goal:** Development environment ready

- [ ] Install Cursor IDE
- [ ] Set up Raspberry Pi 5 with OS
- [ ] Install all dependencies
- [ ] Connect Insta360 Link 2 (verify UVC mode)
- [ ] Test camera: verify gesture recognition works
- [ ] Test microphone (camera's AI noise canceling)
- [ ] Verify Ollama + Llama 3.2 working
- [ ] Create project structure

**Camera Setup Verification:**
```bash
# Check camera detection
v4l2-ctl --list-devices
# Should show: Insta360 Link 2

# Test video capture
ffmpeg -f v4l2 -i /dev/video0 -frames 1 test.jpg

# Verify gesture detection (camera's on-board AI)
# Wave at camera - LED should blink confirming gesture
```

### Phase 1: Voice Loop (Weeks 2-4)
**Goal:** Working voice conversation

**Milestones:**
- [ ] Wake word detection ("Hey Zema")
- [ ] Voice activity detection (VAD)
- [ ] Speech-to-text (Whisper) using camera's mic
- [ ] Basic LLM integration (Ollama)
- [ ] Text-to-speech (Piper)
- [ ] Audio playback
- [ ] Simple conversation (ask/respond)

**Test:** "Hey Zema, what time is it?" → Gets correct response

### Phase 2: Vision (Weeks 5-7)
**Goal:** Camera integration and object detection

**Milestones:**
- [ ] Camera capture from Insta360 Link 2 (UVC mode)
- [ ] Object detection (YOLO)
- [ ] Scene description
- [ ] Gesture recognition integration (camera's AI chip)
- [ ] Test PTZ control (pan/tilt for tracking)
- [ ] Vision-language integration
- [ ] Low-light performance testing (f/1.8 advantage)

**Test:** "Zema, what do you see?" → Describes room accurately
**Test:** Wave at camera → Activates without wake word

### Phase 3: Personal Assistant (Weeks 8-10)
**Goal:** Task management and reminders

**Milestones:**
- [ ] Calendar/scheduling system
- [ ] Reminders and timers
- [ ] Note-taking
- [ ] Task lists
- [ ] Context persistence

**Test:** Set reminder, power off, power on → Reminder still there

### Phase 4: Advanced Vision (Weeks 11-13)
**Goal:** Measurement and 3D modeling

**Milestones:**
- [ ] Object measurement (using calibrated focal length)
- [ ] Basic 3D model generation
- [ ] STL/OBJ export
- [ ] Vision-assisted tasks
- [ ] AI tracking testing (follows you around room)

**Test:** Take photo of object → Generate 3D model file
**Test:** Camera tracks you as you move around

### Phase 5: Ethiopian Integration (Weeks 14-16)
**Goal:** Cultural features and Amharic support

**Milestones:**
- [ ] Amharic speech recognition
- [ ] Amharic TTS
- [ ] Ethiopian calendar
- [ ] Cultural knowledge base
- [ ] Recipe assistance with vision (identify ingredients)

**Test:** Code-switch conversation (English + Amharic)

### Phase 6: Family & Polish (Weeks 17-20)
**Goal:** Multi-user support and refinement

**Milestones:**
- [ ] User profiles
- [ ] Voice recognition for family
- [ ] AI tracking per-user preferences
- [ ] Parental controls
- [ ] Privacy modes
- [ ] Performance optimization
- [ ] Bug fixes and polish

**Test:** Family members can use successfully
**Test:** Camera tracks different family members

---

## 7. Success Criteria

### Technical Performance

**Response Time**
- Wake word detection: <500ms
- Gesture detection: <300ms (camera's AI chip)
- Speech-to-text: <1 second
- AI response generation: <3 seconds (local)
- Text-to-speech: <1 second
- **Total end-to-end: <5 seconds** for simple queries

**Accuracy**
- Speech recognition: >90% word accuracy (English, AI noise canceling)
- Speech recognition: >85% word accuracy (Amharic)
- Object detection: >90% accuracy (better sensor quality)
- Gesture recognition: >95% accuracy (hardware AI chip)
- Wake word false positives: <1 per day
- AI tracking: follows person smoothly without jitter

**Reliability**
- Uptime: 99%+ (only down during updates)
- Crash recovery: Auto-restart within 10 seconds
- Data integrity: Zero data loss
- Battery life: 4+ hours on portable battery (5W camera is efficient)
- Thermal: Camera stays <60°C under continuous use

### User Experience

**Ease of Use**
- Setup time: <10 minutes for new user
- Voice commands: Natural language (no memorization)
- Gesture commands: Intuitive (wave, thumbs up)
- Error recovery: Helpful error messages
- Family adoption: Kids/spouse can use without training

**Privacy & Control**
- Clear data access: View all stored data easily
- Quick deletion: "Delete everything" works instantly
- Privacy modes: Visual indicators (camera LED) always visible
- Audit trail: Know what was processed/stored

### Feature Completeness

**Must-Have (MVP)**
- [x] Voice conversation (English)
- [x] Wake word activation
- [x] Gesture activation (hardware AI)
- [x] Scene description
- [x] Reminders and timers
- [x] Note-taking
- [x] Offline operation

**Should-Have (v1.0)**
- [ ] Amharic support
- [ ] Object measurement (accurate with calibrated lens)
- [ ] Calendar integration
- [ ] Advanced gesture control
- [ ] AI tracking
- [ ] Family profiles

**Nice-to-Have (v1.1+)**
- [ ] 3D modeling
- [ ] Smart home control
- [ ] Recipe guidance with ingredient recognition
- [ ] Advanced voice recognition
- [ ] Cloud sync (optional)

---

## Hardware Advantages Summary

### Insta360 Link 2 Benefits for Zema:

✅ **On-Device AI Processing** - Gesture recognition runs on camera's chip, not Pi CPU  
✅ **Superior Image Quality** - Larger 1/2" sensor, f/1.8 aperture, Phase Detect AF  
✅ **Better Low-Light** - Works in dim rooms (evening use, offices)  
✅ **Accurate Measurements** - Calibrated lens with minimal distortion  
✅ **Zero Pi CPU Overhead** - AI tracking handled by camera  
✅ **True Plug-and-Play** - UVC compliant, no vendor software needed  
✅ **Privacy-First** - All processing on-device, no cloud calls  
✅ **Reliable** - Stable firmware, proven Linux compatibility  
✅ **Cool Running** - Only 5W power, low heat in Pi enclosure  
✅ **AI Noise Canceling** - Cleaner audio for speech recognition  

**Investment Justified:** $140 premium over OBSBOT saves Pi CPU for AI tasks, provides better vision accuracy, and enables true offline operation.

---

## Next Steps

1. **Review this document** - Make sure the vision aligns with your needs
2. **Order hardware** - Raspberry Pi 5 + Insta360 Link 2
3. **Read the Implementation Guide** - See detailed code structure
4. **Read the Infrastructure Guide** - Raspberry Pi setup with Link 2
5. **Start Phase 1** - Begin with voice loop using Cursor prompts
6. **Iterate and test** - Build incrementally, test often

---

## Document Management

**Living Document:** This PRD should be updated as the project evolves.

**Related Documents:**
- Implementation Guide: ZEMA-IMPLEMENTATION.md
- Infrastructure Guide: ZEMA-INFRASTRUCTURE.md
- Cursor Prompts: ZEMA-CURSOR-PROMPTS.md (coming soon)

**Version History:**
- v1.0 (2025-11-01): Initial personal assistant vision (EMEET PIXY)
- v1.1 (2025-11-01): Updated to Insta360 Link 2 based on technical analysis
- Updates will be logged here as project evolves

---

*This is YOUR project. Build it YOUR way. Zema adapts to you, not the other way around.*