from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from database.models import db, User, Scan
from services.nlp_service import nlp_service
from services.audio_service import audio_service
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/smartshield.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-cyber-key'

db.init_app(app)
jwt = JWTManager(app)

# Create database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

# API Endpoints
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created"}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/api/scan/text', methods=['POST'])
@jwt_required()
def scan_text():
    current_user_id = get_jwt_identity()
    data = request.json
    text = data.get('text', '')
    scan_type = data.get('type', 'email') # email, whatsapp, call_transcript
    
    result, confidence = nlp_service.predict(text)
    
    scan = Scan(user_id=current_user_id, scan_type=scan_type, content_summary=text[:100], result=result, confidence=confidence)
    db.session.add(scan)
    db.session.commit()
    
    return jsonify({
        "result": result,
        "confidence": confidence,
        "type": scan_type
    })

@app.route('/api/scan/voice', methods=['POST'])
@jwt_required()
def scan_voice():
    current_user_id = get_jwt_identity()
    if 'file' not in request.files:
        return jsonify({"msg": "No file part"}), 400
    
    file = request.files['file']
    # In a real app, save file and process. Here we simulate.
    result, confidence = audio_service.predict_voice(file.filename)
    
    scan = Scan(user_id=current_user_id, scan_type='voice', content_summary=file.filename, result=result, confidence=confidence)
    db.session.add(scan)
    db.session.commit()
    
    return jsonify({
        "result": result,
        "confidence": confidence
    })

@app.route('/api/user/stats', methods=['GET'])
@jwt_required()
def get_stats():
    current_user_id = get_jwt_identity()
    scans = Scan.query.filter_by(user_id=current_user_id).all()
    
    total = len(scans)
    spam = len([s for s in scans if s.result.lower() in ['spam', 'fraud', 'ai-generated / suspicious']])
    
    return jsonify({
        "total_scans": total,
        "spam_detected": spam,
        "safe_scans": total - spam,
        "recent_scans": [{"type": s.scan_type, "result": s.result, "confidence": s.confidence, "date": s.created_at} for s in scans[-5:]]
    })

if __name__ == '__main__':
    app.run(debug=True)
