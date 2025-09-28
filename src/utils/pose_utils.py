"""
Utility functions for pose detection and angle calculations.
"""

import numpy as np
import cv2
import mediapipe as mp


def calculate_angle(point_a, point_b, point_c):
    """
    Calculate angle between three points.
    
    Args:
        point_a: First point [x, y]
        point_b: Middle point (vertex) [x, y]  
        point_c: End point [x, y]
        
    Returns:
        float: Angle in degrees
    """
    a = np.array(point_a)
    b = np.array(point_b)
    c = np.array(point_c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle


def extract_landmarks(results, mp_pose):
    """
    Extract pose landmarks from MediaPipe results.
    
    Args:
        results: MediaPipe pose detection results
        mp_pose: MediaPipe pose solution
        
    Returns:
        dict: Dictionary containing landmark coordinates
    """
    if not results.pose_landmarks:
        return None
        
    landmarks = results.pose_landmarks.landmark
    
    return {
        'left_shoulder': [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y],
        'left_elbow': [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y],
        'left_wrist': [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y],
        'right_shoulder': [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y],
        'right_elbow': [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y],
        'right_wrist': [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                       landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
    }


def draw_angle_text(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, 
                   font_scale=1, color=(255, 255, 255), thickness=2):
    """
    Draw text on image at specified position.
    
    Args:
        image: OpenCV image
        text: Text to display
        position: Position tuple (x, y)
        font: Font type
        font_scale: Font scale
        color: Text color (BGR)
        thickness: Text thickness
    """
    cv2.putText(image, text, position, font, font_scale, color, thickness, cv2.LINE_AA)


def setup_camera(camera_index=0):
    """
    Initialize camera capture.
    
    Args:
        camera_index: Camera index (default 0)
        
    Returns:
        cv2.VideoCapture: Camera capture object
        
    Raises:
        RuntimeError: If camera cannot be opened
    """
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise RuntimeError(f"Error: Could not open camera at index {camera_index}")
    return cap


def setup_window(window_name, fullscreen=True):
    """
    Setup OpenCV window with specified properties.
    
    Args:
        window_name: Name of the window
        fullscreen: Whether to make window fullscreen
    """
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    if fullscreen:
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)