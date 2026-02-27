import joblib
import os
import re

# Mock classes to handle missing dependencies if needed
class MockVectorizer:
    def transform(self, text): return None

class MockModel:
    def predict_proba(self, text): return [[0.1, 0.9]] # 90% confidence
    def predict(self, text): return [1] # Spam

class NLPService:
    def __init__(self):
        self.model_path = 'models/spam_detector_model.pkl'
        self.vectorizer_path = 'models/tfidf_vectorizer.pkl'
        
        if os.path.exists(self.model_path) and os.path.exists(self.vectorizer_path):
            try:
                self.model = joblib.load(self.model_path)
                self.vectorizer = joblib.load(self.vectorizer_path)
            except:
                self.model = MockModel()
                self.vectorizer = MockVectorizer()
        else:
            self.model = MockModel()
            self.vectorizer = MockVectorizer()

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return text

    def predict(self, text):
        clean_text = self.clean_text(text)
        
        # In mock mode, we use some basic rules for "detection"
        spam_keywords = ['win', 'prize', 'gift card', 'urgent', 'suspended', 'verify', 'click here', 'rich', 'free']
        is_spam = any(keyword in clean_text for keyword in spam_keywords)
        
        if isinstance(self.model, MockModel):
            confidence = 85.0 if is_spam else 12.0
            return ("Spam" if is_spam else "Not Spam"), confidence
        
        # Real prediction
        tfidf = self.vectorizer.transform([clean_text])
        prob = self.model.predict_proba(tfidf)[0]
        prediction = self.model.predict(tfidf)[0]
        
        label = "Spam" if prediction == 1 else "Not Spam"
        confidence = round(prob[prediction] * 100, 2)
        
        return label, confidence

nlp_service = NLPService()
