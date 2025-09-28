#!/usr/bin/env python3
"""
Setup script for AI Fitness Trainer installation and verification.
"""

import os
import subprocess
import sys


def check_python_version():
    """Check if Python version is adequate."""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def check_camera():
    """Check camera availability."""
    print("\n📷 Checking camera availability...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("✅ Camera is available")
            cap.release()
            return True
        else:
            print("⚠️ Camera not detected (you can still run the demo)")
            return False
    except ImportError:
        print("❌ OpenCV not installed properly")
        return False


def check_tts():
    """Check text-to-speech availability."""
    print("\n🗣️ Checking text-to-speech...")
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("✅ Text-to-speech is available")
        engine.stop()
        return True
    except Exception as e:
        print(f"⚠️ TTS warning: {e}")
        print("   The app will work with text feedback instead of speech")
        return False


def run_tests():
    """Run basic functionality tests."""
    print("\n🧪 Running functionality tests...")
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Import main modules
    try:
        from src.utils.pose_utils import calculate_angle
        from src.utils.tts import TTSEngine
        print("✅ Test 1/4: Core module imports")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Test 1/4: Import failed - {e}")
    
    # Test 2: Exercise imports
    try:
        from src.exercises.shoulder_press import ShoulderPressTracker
        from src.exercises.bicep_curl import BicepCurlTracker
        print("✅ Test 2/4: Exercise module imports")
        tests_passed += 1
    except ImportError as e:
        print(f"❌ Test 2/4: Exercise import failed - {e}")
    
    # Test 3: Configuration
    try:
        import config
        assert hasattr(config, 'ANGLE_THRESHOLDS')
        print("✅ Test 3/4: Configuration loaded")
        tests_passed += 1
    except (ImportError, AssertionError) as e:
        print(f"❌ Test 3/4: Configuration failed - {e}")
    
    # Test 4: Angle calculation
    try:
        from src.utils.pose_utils import calculate_angle
        angle = calculate_angle([0, 1], [0, 0], [1, 0])
        assert 85 < angle < 95  # Should be ~90 degrees
        print("✅ Test 4/4: Angle calculation")
        tests_passed += 1
    except (ImportError, AssertionError) as e:
        print(f"❌ Test 4/4: Angle calculation failed - {e}")
    
    print(f"\n📊 Tests passed: {tests_passed}/{total_tests}")
    return tests_passed == total_tests


def show_usage_info():
    """Show usage information."""
    print("\n" + "="*60)
    print("🎯 AI FITNESS TRAINER - SETUP COMPLETE!")
    print("="*60)
    
    print("\n🚀 Quick Start:")
    print("   python main.py                          # Run with shoulder press")
    print("   python main.py --exercise bicep_curl    # Run with bicep curl")
    print("   python demo.py                          # Run demonstration")
    
    print("\n🏋️ Available Exercises:")
    exercises = [
        "shoulder_press      - Shoulder press tracking",
        "bicep_curl          - Standard bicep curl",
        "alternating_bicep_curl - Alternating bicep curl",
        "tricep_kickback     - Tricep kickback exercise"
    ]
    for exercise in exercises:
        print(f"   • {exercise}")
    
    print("\n⚙️ Configuration:")
    print("   Edit config.py to customize settings")
    
    print("\n📖 Documentation:")
    print("   See README.md for detailed instructions")
    
    print("\n🆘 Troubleshooting:")
    print("   • Camera issues: Check camera permissions and connections")
    print("   • TTS issues: Install espeak or espeak-ng system package")
    print("   • Import errors: Ensure all dependencies are installed")


def main():
    """Run the complete setup process."""
    print("🔧 AI FITNESS TRAINER - SETUP & VERIFICATION")
    print("=" * 50)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        success = False
    
    # Check hardware
    camera_ok = check_camera()
    tts_ok = check_tts()
    
    # Run tests
    if not run_tests():
        success = False
    
    # Show results
    if success:
        print("\n✅ Setup completed successfully!")
        show_usage_info()
        return 0
    else:
        print("\n⚠️ Setup completed with warnings")
        print("   Some features may not work properly")
        show_usage_info()
        return 1


if __name__ == "__main__":
    sys.exit(main())