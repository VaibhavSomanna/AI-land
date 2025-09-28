"""
Base class for exercise detection and tracking.
"""

from abc import ABC, abstractmethod
import cv2
import mediapipe as mp
import numpy as np
from typing import Dict, Tuple, Optional

from ..utils.pose_utils import extract_landmarks, calculate_angle, draw_angle_text
from ..utils.tts import TTSEngine


class ExerciseTracker(ABC):
    """Base class for exercise tracking."""
    
    def __init__(self, name: str, tts_engine: TTSEngine):
        """
        Initialize exercise tracker.
        
        Args:
            name: Name of the exercise
            tts_engine: Text-to-speech engine for feedback
        """
        self.name = name
        self.tts_engine = tts_engine
        self.reps = 0
        self.stage = "initial"
        self.feedback_given = False
        
    @abstractmethod
    def detect_exercise(self, landmarks: Dict, image: np.ndarray) -> Tuple[bool, str]:
        """
        Detect and track exercise progress.
        
        Args:
            landmarks: Dictionary of pose landmarks
            image: Current frame image
            
        Returns:
            Tuple of (rep_completed, feedback_message)
        """
        pass
        
    @abstractmethod
    def get_required_landmarks(self) -> list:
        """Return list of required landmark names for this exercise."""
        pass
        
    def reset_exercise(self):
        """Reset exercise state."""
        self.reps = 0
        self.stage = "initial"
        self.feedback_given = False
        
    def get_stats(self) -> Dict:
        """Get current exercise statistics."""
        return {
            'name': self.name,
            'reps': self.reps,
            'stage': self.stage
        }
        
    def provide_feedback(self, message: str, force: bool = False):
        """
        Provide audio feedback to user.
        
        Args:
            message: Feedback message
            force: Force feedback even if recently given
        """
        if force or not self.feedback_given:
            self.tts_engine.speak(message)
            self.feedback_given = True
            
    def draw_exercise_info(self, image: np.ndarray, landmarks: Dict):
        """
        Draw exercise information on the image.
        
        Args:
            image: Image to draw on
            landmarks: Pose landmarks
        """
        # Draw rep count
        draw_angle_text(image, f"Reps: {self.reps}", (10, 30))
        draw_angle_text(image, f"Stage: {self.stage}", (10, 70))
        draw_angle_text(image, f"Exercise: {self.name}", (10, 110))