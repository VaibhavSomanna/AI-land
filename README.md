# AI Fitness Trainer

A real-time AI-powered personal fitness trainer that uses computer vision to track exercise form and provide audio feedback. The system uses MediaPipe for pose detection, OpenCV for video processing, and pyttsx3 for text-to-speech feedback.

## Features

- **Real-time pose detection** using MediaPipe
- **Exercise form tracking** with angle calculations
- **Audio feedback** for proper exercise execution
- **Multiple exercise types** supported:
  - Shoulder Press
  - Bicep Curl
  - Alternating Bicep Curl
  - Tricep Kickback
- **Repetition counting** with visual display
- **Real-time angle visualization** on screen
- **Modular, extensible architecture**

## Installation

### Prerequisites

- Python 3.7 or higher
- Webcam or camera device
- Speakers or headphones for audio feedback

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VaibhavSomanna/AI-land.git
   cd AI-land
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify camera access:**
   Make sure your camera is working and not being used by other applications.

## Usage

### Quick Start

Run the application with the default shoulder press exercise:
```bash
python main.py
```

### Select Different Exercises

Choose a specific exercise type:
```bash
python main.py --exercise shoulder_press
python main.py --exercise bicep_curl
python main.py --exercise alternating_bicep_curl
python main.py --exercise tricep_kickback
```

### Controls

- **'q'** - Quit the application
- **'r'** - Reset exercise counter

## Exercise Instructions

### 1. Shoulder Press
- **Starting position:** Arms in L-shape (90° angles)
- **Movement:** Push both arms straight up until fully extended
- **Return:** Lower arms back to L-shape position
- **Feedback:** Audio cues for proper form and rep counting

### 2. Bicep Curl
- **Starting position:** Arms fully extended (straight down)
- **Movement:** Curl both arms up simultaneously
- **Return:** Lower arms back to extended position
- **Feedback:** Form corrections and rep counting

### 3. Alternating Bicep Curl
- **Starting position:** Arms fully extended
- **Movement:** Curl one arm at a time, alternating left and right
- **Pattern:** Left arm curl → Right arm curl → Repeat
- **Feedback:** Guidance for alternating pattern

### 4. Tricep Kickback
- **Starting position:** Arms bent at elbow (30° angle)
- **Movement:** Extend one arm back fully, then return
- **Pattern:** Alternates between left and right arms
- **Feedback:** Form cues for proper extension

## Project Structure

```
AI-land/
├── main.py                     # Main application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── src/
│   ├── __init__.py
│   ├── exercises/              # Exercise tracking modules
│   │   ├── __init__.py
│   │   ├── base_exercise.py    # Base exercise class
│   │   ├── shoulder_press.py   # Shoulder press tracker
│   │   ├── bicep_curl.py       # Bicep curl tracker
│   │   ├── alternating_bicep_curl.py  # Alternating bicep curl
│   │   └── tricep_kickback.py  # Tricep kickback tracker
│   ├── utils/                  # Utility modules
│   │   ├── __init__.py
│   │   ├── pose_utils.py       # Pose detection utilities
│   │   └── tts.py             # Text-to-speech engine
│   └── ui/                     # UI components (future expansion)
│       └── __init__.py
└── PERSONAL AI FITNESS TRAINER.ipynb  # Original notebook (legacy)
```

## Configuration

You can modify settings in `config.py`:

- **Camera settings:** Camera index, resolution
- **Pose detection:** Confidence thresholds
- **Audio settings:** Speech rate, volume
- **Exercise thresholds:** Angle thresholds for different exercises
- **UI settings:** Font, colors, display options

## Troubleshooting

### Common Issues

1. **Camera not detected:**
   - Check if camera is connected and working
   - Try different camera indices in config.py
   - Ensure no other applications are using the camera

2. **Audio not working:**
   - Check system audio settings
   - Verify speakers/headphones are connected
   - Try adjusting TTS volume in config.py

3. **Poor pose detection:**
   - Ensure good lighting conditions
   - Stand at appropriate distance from camera
   - Wear contrasting clothing
   - Adjust detection confidence in config.py

4. **Import errors:**
   - Verify all dependencies are installed: `pip install -r requirements.txt`
   - Check Python version (3.7+ required)

### Performance Tips

- **Good lighting:** Ensure adequate lighting for better pose detection
- **Camera position:** Position camera to capture full upper body
- **Background:** Use a plain background for better detection
- **Clothing:** Wear fitted clothing for accurate landmark detection

## Development

### Adding New Exercises

1. Create a new exercise class in `src/exercises/`
2. Inherit from `ExerciseTracker` base class
3. Implement required methods:
   - `detect_exercise()`
   - `get_required_landmarks()`
4. Add exercise to main application choices
5. Update configuration with exercise-specific thresholds

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Dependencies

- **opencv-python (>=4.5.0):** Computer vision and video processing
- **mediapipe (>=0.10.0):** Pose detection and landmark extraction
- **numpy (>=1.21.0):** Numerical computations and array operations
- **pyttsx3 (>=2.90):** Text-to-speech conversion

## License

This project is open source. Please check the repository for license details.

## Acknowledgments

- MediaPipe team for pose detection technology
- OpenCV community for computer vision tools
- Contributors and testers

## Support

For issues, questions, or contributions, please visit the GitHub repository or create an issue.
