from flask import jsonify, request, current_app
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.api import bp
from app.decorators import admin_required, hospital_required
from app.fl_globals import aggregator
from app.fl.client import FLClient
import os

# Mapping hospital IDs to data files
HOSPITAL_DATA_MAP = {
    1: 'heart_disease_dataset/hospital_client1.csv',
    2: 'heart_disease_dataset/hospital_client2.csv',
    3: 'heart_disease_dataset/hospital_client3.csv'
}

@bp.route('/fl/status', methods=['GET'])
@login_required
def fl_status():
    return jsonify({
        'round': aggregator.round,
        'clients_updated': len(aggregator.client_weights)
    })

@bp.route('/fl/start_round', methods=['POST'])
@login_required
@admin_required
def start_round():
    # In a real system, this would trigger model distribution.
    # Here, we just clear previous round state if any
    # and maybe re-initialize if round 0.
    if aggregator.round == 0:
        aggregator.initialize_global_model()
    
    return jsonify({'message': f'Round {aggregator.round + 1} started. Waiting for clients.'})

@bp.route('/fl/train', methods=['POST'])
@login_required
@hospital_required
def train_local():
    # Simulate client training
    # For this demo, the server acts as the client too.
    
    data_path = None
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            data_path = upload_path

    # Get latest global model
    global_model = aggregator.get_global_model()
    
    # Train
    # We use a simulated client for now (e.g., Client 1)
    # In real app, we would identify client by current_user.hospital_id
    try:
        # Default to hospital 1 data if no file uploaded
        default_data_path = HOSPITAL_DATA_MAP.get(1)
        client = FLClient(client_id=1, data_path=default_data_path) 
        weights, n_samples = client.train(global_model.get_weights(), data_path=data_path)
        
        # Send update to aggregator
        aggregator.add_client_update(weights, n_samples)
        
        return jsonify({'message': 'Local training complete. Update sent to server.', 'samples': n_samples})
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()}), 500

@bp.route('/fl/aggregate', methods=['POST'])
@login_required
@admin_required
def aggregate():
    if aggregator.aggregate():
        return jsonify({'message': 'Global model updated successfully.'})
    else:
        return jsonify({'error': 'No client updates to aggregate.'}), 400

@bp.route('/fl/history', methods=['GET'])
@login_required
def fl_history():
    return jsonify(aggregator.history)

# --- User Management APIs ---

from app.models import User, Role, Hospital
from app import db

@bp.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    users = User.query.all()
    user_list = []
    for u in users:
        user_list.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'role': u.role.name if u.role else 'None',
            'hospital': u.hospital.name if u.hospital else 'None'
        })
    return jsonify(user_list)

@bp.route('/users', methods=['POST'])
@login_required
@admin_required
def create_user():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    role = Role.query.filter_by(name=data['role']).first()
    if not role:
        return jsonify({'error': 'Invalid role'}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    user.role = role
    
    if data.get('hospital_id'):
        user.hospital_id = data['hospital_id']
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/users/<int:user_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        return jsonify({'error': 'Cannot delete yourself'}), 400
        
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
        
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
