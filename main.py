"""
Main application for AI Fitness Trainer.
"""

import cv2
import mediapipe as mp
import sys
import argparse
from typing import Optional, Dict

from src.exercises.shoulder_press import ShoulderPressTracker
from src.exercises.bicep_curl import BicepCurlTracker
from src.exercises.alternating_bicep_curl import AlternatingBicepCurlTracker
from src.exercises.tricep_kickback import TricepKickbackTracker
from src.utils.tts import TTSEngine
from src.utils.pose_utils import setup_camera, setup_window, extract_landmarks
from config import *


class FitnessTrainerApp:
    """Main application class for AI Fitness Trainer."""
    
    def __init__(self, exercise_type: str = "shoulder_press"):
        """
        Initialize the fitness trainer app.
        
        Args:
            exercise_type: Type of exercise to track
        """
        self.exercise_type = exercise_type
        self.tts_engine = TTSEngine(TTS_RATE, TTS_VOLUME)
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Initialize exercise tracker
        self.exercise_tracker = self._create_exercise_tracker()
        
        # Setup camera and window
        self.cap = setup_camera(CAMERA_INDEX)
        self.window_name = f"AI Fitness Trainer - {self.exercise_tracker.name}"
        setup_window(self.window_name, WINDOW_FULLSCREEN)
        
    def _create_exercise_tracker(self):
        """Create exercise tracker based on type."""
        trackers = {
            "shoulder_press": ShoulderPressTracker,
            "bicep_curl": BicepCurlTracker,
            "alternating_bicep_curl": AlternatingBicepCurlTracker,
            "tricep_kickback": TricepKickbackTracker
        }
        
        if self.exercise_type not in trackers:
            raise ValueError(f"Unknown exercise type: {self.exercise_type}")
            
        return trackers[self.exercise_type](self.tts_engine)
        
    def run(self):
        """Run the main application loop."""
        print(f"Starting AI Fitness Trainer - {self.exercise_tracker.name}")
        print("Press 'q' to quit, 'r' to reset exercise counter")
        
        # Welcome message
        self.tts_engine.speak(f"Welcome to AI Fitness Trainer. Starting {self.exercise_tracker.name} tracking.")
        
        with self.mp_pose.Pose(
            min_detection_confidence=MIN_DETECTION_CONFIDENCE,
            min_tracking_confidence=MIN_TRACKING_CONFIDENCE
        ) as pose:
            
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame from camera")
                    break
                    
                # Process frame
                image = self._process_frame(frame, pose)
                
                # Display frame
                cv2.imshow(self.window_name, image)
                
                # Handle key presses
                key = cv2.waitKey(10) & 0xFF
                if key == ord('q'):
                    break
                elif key == ord('r'):
                    self.exercise_tracker.reset_exercise()
                    self.tts_engine.speak("Exercise counter reset")
                    
        self._cleanup()
        
    def _process_frame(self, frame, pose):
        """
        Process a single frame for pose detection and exercise tracking.
        
        Args:
            frame: Input video frame
            pose: MediaPipe pose detector
            
        Returns:
            Processed frame with annotations
        """
        # Convert to RGB for MediaPipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        # Detect pose
        results = pose.process(image)
        
        # Convert back to BGR for OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            # Extract landmarks
            landmarks = extract_landmarks(results, self.mp_pose)
            
            if landmarks:
                # Track exercise
                rep_completed, feedback = self.exercise_tracker.detect_exercise(landmarks, image)
                
                # Provide feedback if available
                if feedback:
                    self.exercise_tracker.provide_feedback(feedback)
                    
                # Draw exercise info
                self.exercise_tracker.draw_exercise_info(image, landmarks)
                
            # Draw pose landmarks
            self.mp_drawing.draw_landmarks(
                image, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS
            )
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            
        return image
        
    def _cleanup(self):
        """Clean up resources."""
        print("Cleaning up...")
        self.cap.release()
        cv2.destroyAllWindows()
        self.tts_engine.cleanup()
        print("Goodbye!")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AI Fitness Trainer")
    parser.add_argument(
        "--exercise", 
        choices=["shoulder_press", "bicep_curl", "alternating_bicep_curl", "tricep_kickback"],
        default="shoulder_press",
        help="Type of exercise to track"
    )
    
    args = parser.parse_args()
    
    try:
        app = FitnessTrainerApp(args.exercise)
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()