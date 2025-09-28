"""
Text-to-speech functionality for exercise feedback.
"""

from typing import Optional

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False


class TTSEngine:
    """Text-to-Speech engine wrapper for exercise feedback."""
    
    def __init__(self, rate: int = 150, volume: float = 0.9):
        """
        Initialize TTS engine.
        
        Args:
            rate: Speech rate in words per minute
            volume: Speech volume (0.0 to 1.0)
        """
        self.rate = rate
        self.volume = volume
        self.tts_available = TTS_AVAILABLE
        
        if self.tts_available:
            try:
                self.engine = pyttsx3.init()
                self.set_rate(rate)
                self.set_volume(volume)
            except Exception as e:
                print(f"Warning: TTS engine failed to initialize: {e}")
                self.tts_available = False
                self.engine = None
        else:
            print("Warning: pyttsx3 not available, TTS disabled")
            self.engine = None
        
    def set_rate(self, rate: int):
        """Set speech rate."""
        self.rate = rate
        if self.engine:
            self.engine.setProperty('rate', rate)
        
    def set_volume(self, volume: float):
        """Set speech volume."""
        self.volume = volume
        if self.engine:
            self.engine.setProperty('volume', volume)
        
    def speak(self, text: str, wait: bool = True):
        """
        Speak the given text.
        
        Args:
            text: Text to speak
            wait: Whether to wait for speech to complete
        """
        if self.engine and self.tts_available:
            try:
                self.engine.say(text)
                if wait:
                    self.engine.runAndWait()
            except Exception as e:
                print(f"TTS Error: {e}")
                print(f"Message: {text}")
        else:
            print(f"🗣️ TTS: {text}")
            
    def speak_async(self, text: str):
        """Speak text asynchronously."""
        self.speak(text, wait=False)
        
    def stop(self):
        """Stop current speech."""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
        
    def cleanup(self):
        """Clean up TTS engine resources."""
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass