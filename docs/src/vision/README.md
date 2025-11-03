# Vision Module Documentation

## Purpose
The `src/vision/` folder handles all vision/computer vision functionality: camera interface, object detection, scene analysis, gesture detection, measurements, and 3D model generation.

## Files in This Folder

### `camera.py`
Camera interface for Insta360 Link 2. Handles video capture, PTZ controls (pan/tilt), autofocus, and frame capture.

### `detector.py`
Object detection using YOLOv8. Detects objects in camera frames and returns bounding boxes with labels and confidence scores.

### `analyzer.py`
Scene analyzer that combines object detection with LLM to generate natural language descriptions of scenes.

### `gestures.py`
Gesture detection from camera. Primary method: LED blink detection. Fallback: MediaPipe hand detection.

### `measurement.py`
Measurement system for measuring object dimensions using camera calibration and distance estimation.

### `model3d.py`
3D model generator. Creates 3D models from photos using photogrammetry techniques.

## Vision Flow
```
Camera → Frame Capture → Detector → Objects → Analyzer → Description
                                    ↓
                              Gestures → Gesture Type
                                    ↓
                              Measurement → Dimensions
```

## Key Features
- PTZ camera control
- Object detection (YOLOv8)
- Scene description
- Gesture recognition
- Dimension measurement
- 3D model generation

