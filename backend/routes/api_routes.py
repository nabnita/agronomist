"""
API routes for AgroMind AI
"""
from flask import Blueprint, request, jsonify
from typing import Dict, Any
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.ml_service import get_ml_service
from services.explainer_service import get_explainer_service
from services.ai_agronomist import get_ai_agronomist
from services.sustainability_service import get_sustainability_service
from utils.validators import validate_soil_climate_input, validate_crop_name, sanitize_input

# Create blueprint
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/predict', methods=['POST'])
def predict():
    """
    Predict top 3 crops based on soil and climate parameters
    
    Request body:
    {
        "N": 90,
        "P": 42,
        "K": 43,
        "pH": 6.5,
        "temperature": 20.8,
        "humidity": 82,
        "rainfall": 202
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Sanitize input
        data = sanitize_input(data)
        
        # Validate input
        is_valid, error_msg = validate_soil_climate_input(data)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Get ML service and predict
        ml_service = get_ml_service()
        predictions = ml_service.predict_top_crops(data, n=3)
        
        return jsonify({
            'success': True,
            'predictions': predictions,
            'input': data
        })
    
    except Exception as e:
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@api.route('/explain', methods=['POST'])
def explain():
    """
    Explain why a specific crop was recommended
    
    Request body:
    {
        "N": 90,
        "P": 42,
        "K": 43,
        "pH": 6.5,
        "temperature": 20.8,
        "humidity": 82,
        "rainfall": 202,
        "crop": "rice"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract crop
        crop = data.get('crop')
        if not crop:
            return jsonify({'error': 'Crop name is required'}), 400
        
        # Validate crop
        ml_service = get_ml_service()
        valid_crops = ml_service.get_all_crops()
        is_valid, error_msg = validate_crop_name(crop, valid_crops)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Sanitize and validate soil/climate data
        features = sanitize_input({
            k: v for k, v in data.items() if k != 'crop'
        })
        is_valid, error_msg = validate_soil_climate_input(features)
        if not is_valid:
            return jsonify({'error': error_msg}), 400
        
        # Get explanation
        explainer_service = get_explainer_service()
        explanation = explainer_service.explain_prediction(features, crop)
        
        return jsonify({
            'success': True,
            'explanation': explanation
        })
    
    except Exception as e:
        return jsonify({'error': f'Explanation error: {str(e)}'}), 500

@api.route('/ai-advice', methods=['POST'])
def ai_advice():
    """
    Get AI agronomist advice for a crop
    
    Request body:
    {
        "crop": "rice",
        "N": 90,
        "P": 42,
        "K": 43,
        "pH": 6.5,
        "temperature": 20.8,
        "humidity": 82,
        "rainfall": 202,
        "location": "Punjab" (optional)
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract crop
        crop = data.get('crop')
        if not crop:
            return jsonify({'error': 'Crop name is required'}), 400
        
        # Extract location (optional)
        location = data.get('location')
        
        # Prepare soil and climate parameters
        soil_params = {
            'N': data.get('N'),
            'P': data.get('P'),
            'K': data.get('K'),
            'pH': data.get('pH')
        }
        
        climate_params = {
            'temperature': data.get('temperature'),
            'humidity': data.get('humidity'),
            'rainfall': data.get('rainfall')
        }
        
        # Get AI advice
        ai_agronomist = get_ai_agronomist()
        advice = ai_agronomist.get_farming_advice(
            crop, soil_params, climate_params, location
        )
        
        return jsonify(advice)
    
    except Exception as e:
        return jsonify({'error': f'AI advice error: {str(e)}'}), 500

@api.route('/soil-impact', methods=['POST'])
def soil_impact():
    """
    Analyze sustainability and soil impact of growing a crop
    
    Request body:
    {
        "crop": "rice",
        "N": 90,
        "P": 42,
        "K": 43,
        "pH": 6.5,
        "rainfall": 202,
        "duration_months": 4 (optional)
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract crop
        crop = data.get('crop')
        if not crop:
            return jsonify({'error': 'Crop name is required'}), 400
        
        # Prepare soil parameters
        soil_params = {
            'N': data.get('N'),
            'P': data.get('P'),
            'K': data.get('K'),
            'pH': data.get('pH'),
            'rainfall': data.get('rainfall')
        }
        
        # Get duration
        duration = data.get('duration_months', 4)
        
        # Get sustainability analysis
        sustainability_service = get_sustainability_service()
        analysis = sustainability_service.analyze_soil_impact(
            crop, soil_params, duration
        )
        
        return jsonify({
            'success': True,
            'analysis': analysis
        })
    
    except Exception as e:
        return jsonify({'error': f'Sustainability analysis error: {str(e)}'}), 500

@api.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'AgroMind AI',
        'version': '1.0.0'
    })

@api.route('/crops', methods=['GET'])
def get_crops():
    """Get list of all available crops"""
    try:
        ml_service = get_ml_service()
        crops = ml_service.get_all_crops()
        
        return jsonify({
            'success': True,
            'crops': crops,
            'count': len(crops)
        })
    
    except Exception as e:
        return jsonify({'error': f'Error fetching crops: {str(e)}'}), 500
