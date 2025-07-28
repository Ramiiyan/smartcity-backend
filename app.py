from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smartcity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -------------------- MODELS -------------------- #

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citizen_id = db.Column(db.String(100), nullable=False)
    document_type = db.Column(db.String(100), nullable=False)
    issued_date = db.Column(db.DateTime, default=datetime.utcnow)
    content = db.Column(db.Text)  # Could be file path or text

# -------------------- ROUTES -------------------- #

# health check endpoint
@app.route('/')
def index():
    return "SmartCity Citizen Services Backend"

# Create a new service request.
@app.route('/requests', methods=['POST'])
def create_request():
    data = request.get_json()
    service = ServiceRequest(
        citizen_id=data['citizen_id'],
        category=data['category'],
        description=data['description']
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({'message': 'Request created', 'service_id': service.id})

# Retrieve all service requests for a specific citizen.
@app.route('/requests/<int:cid>', methods=['GET'])
def get_requests(cid):
    requests = ServiceRequest.query.filter_by(citizen_id=cid).all()
    return jsonify([{
        'id': r.id,
        'category': r.category,
        'description': r.description,
        'status': r.status,
        'created_at': r.created_at.strftime('%Y-%m-%d %H:%M')
    } for r in requests])

# Add a document for a citizen.
@app.route('/documents', methods=['POST'])
def add_document():
    data = request.get_json()
    doc = Document(
        citizen_id=data['citizen_id'],
        document_type=data['document_type'],
        content=data['content']
    )
    db.session.add(doc)
    db.session.commit()
    return jsonify({'message': 'Document added', 'document_id': doc.id})

# Retrieve all documents for a specific citizen.
@app.route('/documents/<int:cid>', methods=['GET'])
def get_documents(cid):
    docs = Document.query.filter_by(citizen_id=cid).all()
    return jsonify([{
        'id': d.id,
        'document_type': d.document_type,
        'issued_date': d.issued_date.strftime('%Y-%m-%d'),
        'content': d.content
    } for d in docs])

# Update the status of a service request (Admin only).
@app.route('/admin/requests/<int:req_id>', methods=['PUT'])
def update_request_status(req_id):
    req = ServiceRequest.query.get_or_404(req_id)
    data = request.get_json()
    req.status = data.get('status', req.status)
    db.session.commit()
    return jsonify({'message': 'Status updated'})

# Get all service requests (Admin only).
@app.route('/admin/services/requests/', methods=['GET'])
def get_all_requests():
    requests = ServiceRequest.query.all()
    return jsonify([{
        'id': r.id,
        'citizen_id': r.citizen_id,
        'category': r.category,
        'description': r.description,
        'status': r.status,
        'created_at': r.created_at.strftime('%Y-%m-%d %H:%M')
    } for r in requests])



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
