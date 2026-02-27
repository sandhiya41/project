import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords
import re

# Download stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return " ".join(words)

# Sample dataset (Spam vs Ham)
data = {
    'text': [
        "Congratulations! You've won a $1,000 Walmart Gift Card. Click here to claim.",
        "Hi John, are we still meeting for lunch at 12:30?",
        "URGENT: Your account has been suspended. Please log in to verify your identity.",
        "Hey, can you send me that report by EOD?",
        "WINNER! Claim your prize now by calling 0800-spam-me.",
        "Your Amazon order has been shipped and will arrive tomorrow.",
        "Get rich quick! No experience needed. Work from home.",
        "The weather today is expected to be sunny with a high of 75.",
        "Free entry into our weekly competition! Text WIN to 80123.",
        "Are you available for a quick call this afternoon?",
        "Your bank account has a suspicious login attempt. Click here.",
        "Dinner at 7 tonight?",
        "Final reminder: Your subscription expires in 24 hours.",
        "Please find the attached invoice for your recent purchase.",
        "Claim your 50% discount on all luxury watches now!",
        "Can you help me with the project documentation?",
        "You have a new voicemail. Listen here: bit.ly/spam-link",
        "Let's catch up soon.",
        "Investment opportunity! Triple your money in 30 days.",
        "Meeting moved to Room 302."
    ],
    'label': [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)
df['processed_text'] = df['text'].apply(preprocess_text)

# Training
X = df['processed_text']
y = df['label']

vectorizer = TfidfVectorizer()
X_tfidf = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred)}")
print(classification_report(y_test, y_pred))

# Save model and vectorizer
joblib.dump(model, 'models/spam_detector_model.pkl')
joblib.dump(vectorizer, 'models/tfidf_vectorizer.pkl')
print("Model and Vectorizer saved successfully.")
