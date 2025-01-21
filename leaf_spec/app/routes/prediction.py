from flask import Blueprint, request, jsonify
from app.services.prediction_service import PredictionService
from PIL import Image
import io

prediction_bp = Blueprint('prediction', __name__)

@prediction_bp.route('/predict_species', methods=['POST'])
def predict_species():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        image_file = request.files['image']
        image = Image.open(io.BytesIO(image_file.read()))
        
        species, confidence = PredictionService.predict(image)
        
        return jsonify({
            'species': species,
            'confidence': confidence
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
