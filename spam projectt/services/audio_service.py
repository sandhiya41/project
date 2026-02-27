import os
import random

class AudioService:
    def __init__(self):
        self.model_path = 'models/voice_fraud_model.pkl'
        # Librosa is heavy, we'll use a simulated extraction for the demo
    
    def predict_voice(self, file_path):
        # In a real app, we would use librosa.load and feature extraction
        # For this demo, we simulate feature analysis based on filename or random
        
        filename = os.path.basename(file_path).lower()
        
        # Simulated logic
        if 'ai' in filename or 'synth' in filename or 'fake' in filename:
            return "AI-Generated / Suspicious", random.uniform(88, 99)
        
        return "Original / Authentic", random.uniform(92, 99)

audio_service = AudioService()
