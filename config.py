"""
Configuration settings for the AI Fitness Trainer application.
"""

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Pose detection settings
MIN_DETECTION_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# UI settings
WINDOW_FULLSCREEN = True
FONT = 'FONT_HERSHEY_SIMPLEX'
FONT_SCALE = 1
FONT_COLOR = (255, 255, 255)
FONT_THICKNESS = 2

# Text-to-speech settings
TTS_RATE = 150  # Words per minute
TTS_VOLUME = 0.9

# Exercise angle thresholds (in degrees)
ANGLE_THRESHOLDS = {
    'shoulder_press': {
        'start_min': 80,
        'start_max': 100,
        'up_threshold': 160,
        'down_threshold': 90
    },
    'bicep_curl': {
        'start_threshold': 160,
        'up_threshold': 60,
        'down_threshold': 160
    },
    'tricep_kickback': {
        'start_threshold': 30,
        'up_threshold': 150,
        'down_threshold': 30
    }
}