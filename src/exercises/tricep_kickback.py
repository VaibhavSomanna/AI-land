"""
Tricep Kickback exercise tracker.
"""

import numpy as np
from typing import Dict, Tuple

from .base_exercise import ExerciseTracker
from ..utils.pose_utils import calculate_angle, draw_angle_text
from ..utils.tts import TTSEngine
from config import ANGLE_THRESHOLDS


class TricepKickbackTracker(ExerciseTracker):
    """Tracker for tricep kickback exercise."""
    
    def __init__(self, tts_engine: TTSEngine):
        super().__init__("Tricep Kickback", tts_engine)
        self.thresholds = ANGLE_THRESHOLDS['tricep_kickback']
        self.left_stage = "initial"
        self.right_stage = "initial"
        self.current_arm = "left"  # Start with left arm
        
    def get_required_landmarks(self) -> list:
        """Return required landmarks for tricep kickback."""
        return ['left_shoulder', 'left_elbow', 'left_wrist', 
                'right_shoulder', 'right_elbow', 'right_wrist']
                
    def detect_exercise(self, landmarks: Dict, image: np.ndarray) -> Tuple[bool, str]:
        """
        Detect tricep kickback exercise.
        
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
        
        # Left arm logic
        if self.current_arm == "left":
            if (self.left_stage == "initial" and 
                left_angle < self.thresholds['start_threshold']):
                
                self.left_stage = "start"
                feedback = "Start position detected for left arm. Extend your arm fully."
                self.feedback_given = False
                
            elif (self.left_stage == "start" and 
                  left_angle > self.thresholds['up_threshold']):
                  
                self.left_stage = "up"
                self.feedback_given = False
                
            elif (self.left_stage == "up" and 
                  left_angle < self.thresholds['down_threshold']):
                  
                self.left_stage = "initial"
                self.reps += 1
                rep_completed = True
                feedback = f"Left arm tricep kickback completed! Total reps: {self.reps}. Switch to right arm."
                self.current_arm = "right"
                self.feedback_given = False
                
        # Right arm logic
        elif self.current_arm == "right":
            if (self.right_stage == "initial" and 
                right_angle < self.thresholds['start_threshold']):
                
                self.right_stage = "start"
                feedback = "Start position detected for right arm. Extend your arm fully."
                self.feedback_given = False
                
            elif (self.right_stage == "start" and 
                  right_angle > self.thresholds['up_threshold']):
                  
                self.right_stage = "up"
                self.feedback_given = False
                
            elif (self.right_stage == "up" and 
                  right_angle < self.thresholds['down_threshold']):
                  
                self.right_stage = "initial"
                self.reps += 1
                rep_completed = True
                feedback = f"Right arm tricep kickback completed! Total reps: {self.reps}. Switch to left arm."
                self.current_arm = "left"
                self.feedback_given = False
                
        return rep_completed, feedback
        
    def reset_exercise(self):
        """Reset exercise state."""
        super().reset_exercise()
        self.left_stage = "initial"
        self.right_stage = "initial"
        self.current_arm = "left"
        
    def _draw_angles(self, image: np.ndarray, landmarks: Dict, left_angle: float, right_angle: float):
        """Draw angle information on the image."""
        # Draw angles at elbow positions
        left_elbow_pos = tuple(np.multiply(landmarks['left_elbow'], [640, 480]).astype(int))
        right_elbow_pos = tuple(np.multiply(landmarks['right_elbow'], [640, 480]).astype(int))
        
        draw_angle_text(image, str(int(left_angle)), left_elbow_pos)
        draw_angle_text(image, str(int(right_angle)), right_elbow_pos)
        
        # Draw angle values and current arm info
        draw_angle_text(image, f"Left: {int(left_angle)}°", (10, 150))
        draw_angle_text(image, f"Right: {int(right_angle)}°", (10, 190))
        draw_angle_text(image, f"Current arm: {self.current_arm}", (10, 230))
        
        # Highlight current arm
        if self.current_arm == "left":
            draw_angle_text(image, "← ACTIVE", (200, 150), color=(0, 255, 0))
        else:
            draw_angle_text(image, "ACTIVE →", (200, 190), color=(0, 255, 0))