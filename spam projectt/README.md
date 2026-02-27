# SmartShield AI – Universal Spam & Voice Fraud Detector

SmartShield AI is a state-of-the-art cybersecurity platform that leverages Machine Learning and Natural Language Processing to detect fraud across Emails, WhatsApp, Phone Calls, and Voice recordings.

## 🚀 Features
- **Email Spam Detection:** TF-IDF + Logistic Regression analysis.
- **WhatsApp Analysis:** Phishing link and urgency pattern detection.
- **Call Script Scrutiny:** Analyze transcripts for common scam tactics.
- **Voice Manipulation Detection:** MFCC and spectral feature analysis to identify AI-generated voices.
- **Modern Dashboard:** Interactive statistics and scan history with Chart.js.
- **JWT-based Security:** Secure authentication and encrypted communication.

## 🛠️ Tech Stack
- **Frontend:** Vanilla HTML5, CSS3 (Modern UI), JavaScript (ES6).
- **Backend:** Python Flask, SQLAlchemy.
- **AI/ML:** Scikit-learn, joblib (Mock logic fallback included).
- **Security:** Flask-JWT-Extended, Werkzeug for hashing.

## 📦 Setup Instructions
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize the models:
   ```bash
   python models/train_text_model.py
   python models/train_voice_model.py
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open `http://127.0.0.1:5000` in your browser.

## 📂 Project Structure
- `/models`: Training scripts and serialized models.
- `/services`: Core AI logic for NLP and Audio.
- `/static`: CSS styles and frontend assets.
- `/templates`: HTML pages (Dashboard, Auth, Landing).
- `/database`: SQLite storage logic.

## 🚀 Scalability & Deployment
- **Deployment:** Recommended on **Render** (Flask + Gunicorn), **Railway**, or **AWS EC2**.
- **Scalability:** The architecture is designed to be stateless (JWT), allowing easy scaling using a load balancer and a hosted PostgreSQL database instead of SQLite.
- **API:** Fully featured REST API allows for integration with Twilio webhooks or WhatsApp Business API.

## 🔮 Future Improvements
- Real-time Twilio integration for live call monitoring.
- Integration with VirusTotal API for suspicious link scanning.
- Federated learning for improved privacy.
- Browser extension for real-time web mail protection.
