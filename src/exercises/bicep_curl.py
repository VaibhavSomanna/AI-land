"""
Bicep Curl exercise tracker.
"""

import numpy as np
from typing import Dict, Tuple

from .base_exercise import ExerciseTracker
from ..utils.pose_utils import calculate_angle, draw_angle_text
from ..utils.tts import TTSEngine
from config import ANGLE_THRESHOLDS


class BicepCurlTracker(ExerciseTracker):
    """Tracker for bicep curl exercise."""
    
    def __init__(self, tts_engine: TTSEngine):
        super().__init__("Bicep Curl", tts_engine)
        self.thresholds = ANGLE_THRESHOLDS['bicep_curl']
        
    def get_required_landmarks(self) -> list:
        """Return required landmarks for bicep curl."""
        return ['left_shoulder', 'left_elbow', 'left_wrist', 
                'right_shoulder', 'right_elbow', 'right_wrist']
                
    def detect_exercise(self, landmarks: Dict, image: np.ndarray) -> Tuple[bool, str]:
        """
        Detect bicep curl exercise.
        
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
        
        # Check for starting position (arms extended)
        if (self.stage == "initial" and 
            left_angle > self.thresholds['start_threshold'] and 
            right_angle > self.thresholds['start_threshold']):
            
            self.stage = "start"
            feedback = "Start position detected. Curl your arms!"
            self.feedback_given = False
            
        # Check for curl up (arms bent)
        elif (self.stage == "start" and 
              left_angle < self.thresholds['up_threshold'] and 
              right_angle < self.thresholds['up_threshold']):
              
            self.stage = "up"
            self.feedback_given = False
            
        # Check for return to extended position
        elif (self.stage == "up" and 
              left_angle > self.thresholds['down_threshold'] and 
              right_angle > self.thresholds['down_threshold']):
              
            self.stage = "initial"
            self.reps += 1
            rep_completed = True
            feedback = f"Bicep curl completed! Reps: {self.reps}"
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