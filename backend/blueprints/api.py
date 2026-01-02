from flask import Blueprint, request, jsonify
from backend.services.classifier import classifier

api = Blueprint('api', __name__)

@api.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    try:
        image_bytes = file.read()
        results = classifier.predict(image_bytes)
        return jsonify({'predictions': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api.route('/export', methods=['GET'])
def export():
    # Placeholder for export logic. In a real app this might read from a DB.
    # For now, we return a success message or sample data structure.
    return jsonify({'message': 'Export endpoint ready. Implement DB to export stored results.'})
