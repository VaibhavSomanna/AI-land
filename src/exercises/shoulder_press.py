"""
Shoulder Press exercise tracker.
"""

import numpy as np
from typing import Dict, Tuple

from .base_exercise import ExerciseTracker
from ..utils.pose_utils import calculate_angle, draw_angle_text
from ..utils.tts import TTSEngine
from config import ANGLE_THRESHOLDS


class ShoulderPressTracker(ExerciseTracker):
    """Tracker for shoulder press exercise."""
    
    def __init__(self, tts_engine: TTSEngine):
        super().__init__("Shoulder Press", tts_engine)
        self.thresholds = ANGLE_THRESHOLDS['shoulder_press']
        
    def get_required_landmarks(self) -> list:
        """Return required landmarks for shoulder press."""
        return ['left_shoulder', 'left_elbow', 'left_wrist', 
                'right_shoulder', 'right_elbow', 'right_wrist']
                
    def detect_exercise(self, landmarks: Dict, image: np.ndarray) -> Tuple[bool, str]:
        """
        Detect shoulder press exercise.
        
        Args:
            landmarks: Pose landmarks dictionary
            image: Current frame
            
        Returns:
            Tuple of (rep_completed, feedback_message)
        """
        # Calculate angles for both arms
        left_angle = calculate_angle(
            landmarks['left_shoulder'], 
            landmarks['left_elbow'], 
            landmarks['left_wrist']
        )
        right_angle = calculate_angle(
            landmarks['right_shoulder'], 
            landmarks['right_elbow'], 
            landmarks['right_wrist']
        )
        
        # Draw angles on image
        self._draw_angles(image, landmarks, left_angle, right_angle)
        
        # Exercise logic
        rep_completed = False
        feedback = ""
        
        # Check for initial L-shape position
        if (self.stage == "initial" and 
            self.thresholds['start_min'] < left_angle < self.thresholds['start_max'] and
            self.thresholds['start_min'] < right_angle < self.thresholds['start_max']):
            
            self.stage = "start"
            feedback = "Start position detected. Push your arms up!"
            self.feedback_given = False
            
        # Check for full extension
        elif self.stage == "start":
            if (left_angle > self.thresholds['up_threshold'] and 
                right_angle > self.thresholds['up_threshold']):
                self.stage = "up"
                self.feedback_given = False
            elif not self.feedback_given:
                feedback = "Push your arms up fully."
                
        # Check for return to starting position
        elif (self.stage == "up" and 
              left_angle < self.thresholds['down_threshold'] and 
              right_angle < self.thresholds['down_threshold']):
            
            self.stage = "initial"
            self.reps += 1
            rep_completed = True
            feedback = f"Shoulder press completed! Reps: {self.reps}"
            self.feedback_given = False
            
        return rep_completed, feedback
        
    def _draw_angles(self, image: np.ndarray, landmarks: Dict, left_angle: float, right_angle: float):
        """Draw angle information on the image."""
        # Draw angles at elbow positions
        left_elbow_pos = tuple(np.multiply(landmarks['left_elbow'], [640, 480]).astype(int))
        right_elbow_pos = tuple(np.multiply(landmarks['right_elbow'], [640, 480]).astype(int))
        
        draw_angle_text(image, str(int(left_angle)), left_elbow_pos)
        draw_angle_text(image, str(int(right_angle)), right_elbow_pos)
        
        # Draw angle values in corner
        draw_angle_text(image, f"Left: {int(left_angle)}°", (10, 150))
        draw_angle_text(image, f"Right: {int(right_angle)}°", (10, 190))