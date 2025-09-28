"""
Text-to-speech functionality for exercise feedback.
"""

import pyttsx3
from typing import Optional


class TTSEngine:
    """Text-to-Speech engine wrapper for exercise feedback."""
    
    def __init__(self, rate: int = 150, volume: float = 0.9):
        """
        Initialize TTS engine.
        
        Args:
            rate: Speech rate in words per minute
            volume: Speech volume (0.0 to 1.0)
        """
        self.engine = pyttsx3.init()
        self.set_rate(rate)
        self.set_volume(volume)
        
    def set_rate(self, rate: int):
        """Set speech rate."""
        self.engine.setProperty('rate', rate)
        
    def set_volume(self, volume: float):
        """Set speech volume."""
        self.engine.setProperty('volume', volume)
        
    def speak(self, text: str, wait: bool = True):
        """
        Speak the given text.
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete
        """
        self.engine.say(text)
        if wait:
            self.engine.runAndWait()
            
    def speak_async(self, text: str):
        """Speak text asynchronously."""
        self.speak(text, wait=False)
        
    def stop(self):
        """Stop current speech."""
        self.engine.stop()
        
    def cleanup(self):
        """Clean up TTS engine resources."""
        try:
            self.engine.stop()
        except:
            pass