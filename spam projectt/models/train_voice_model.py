import librosa
import numpy as np
import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def extract_features(file_path):
    try:
        y, sr = librosa.load(file_path, duration=3, offset=0.5)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
        mfccs_processed = np.mean(mfccs.T, axis=0)
        
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_centroid_mean = np.mean(spectral_centroid)
        
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        spectral_rolloff_mean = np.mean(spectral_rolloff)
        
        features = np.hstack([mfccs_processed, spectral_centroid_mean, spectral_rolloff_mean])
        return features
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None

# For this simulation, we'll create a dummy classifier since we don't have actual .wav files yet.
# In a real scenario, this would iterate through a directory of real vs fake voices.

def train_dummy_voice_model():
    # Simulated features (42 features: 40 MFCC + 2 spectral)
    X = np.random.rand(100, 42)
    y = np.random.randint(0, 2, 100) # 0: Original, 1: AI-Generated
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    print(f"Voice Model Accuracy: {accuracy_score(y_test, y_pred)}")
    
    joblib.dump(model, 'models/voice_fraud_model.pkl')
    print("Voice model saved successfully.")

if __name__ == "__main__":
    train_dummy_voice_model()
