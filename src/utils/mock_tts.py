"""
Mock TTS engine for demo purposes (when eSpeak is not available).
"""

class MockTTSEngine:
    """Mock TTS engine that doesn't actually speak."""
    
    def __init__(self, rate=150, volume=0.9):
        self.rate = rate
        self.volume = volume
        print("🔇 Using mock TTS engine (eSpeak not available)")
        
    def set_rate(self, rate):
        self.rate = rate
        
    def set_volume(self, volume):
        self.volume = volume
        
    def speak(self, text, wait=True):
        print(f"🗣️ TTS: {text}")
        
    def speak_async(self, text):
        self.speak(text, wait=False)
        
    def stop(self):
        pass
        
    def cleanup(self):
        pass