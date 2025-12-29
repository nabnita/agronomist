"""
Helper utilities for AgroMind AI
"""
import numpy as np
from typing import List, Dict, Any

def format_confidence_score(probability: float) -> str:
    """
    Format probability as percentage string
    
    Args:
        probability: Float between 0 and 1
        
    Returns:
        Formatted percentage string (e.g., "85.3%")
    """
    return f"{probability * 100:.1f}%"

def get_top_n_predictions(probabilities: np.ndarray, labels: List[str], n: int = 3) -> List[Dict[str, Any]]:
    """
    Get top N predictions with confidence scores
    
    Args:
        probabilities: Array of probabilities for each class
        labels: List of class labels
        n: Number of top predictions to return
        
    Returns:
        List of dicts with crop name and confidence
    """
    # Get indices of top N probabilities
    top_indices = np.argsort(probabilities)[-n:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            'crop': labels[idx],
            'confidence': float(probabilities[idx]),
            'confidence_percent': format_confidence_score(probabilities[idx])
        })
    
    return results

def create_feature_dict(N: float, P: float, K: float, pH: float, 
                       temperature: float, humidity: float, rainfall: float) -> Dict[str, float]:
    """
    Create feature dictionary from individual parameters
    
    Args:
        N, P, K, pH, temperature, humidity, rainfall: Soil and climate parameters
        
    Returns:
        Dictionary with feature names and values
    """
    return {
        'N': N,
        'P': P,
        'K': K,
        'pH': pH,
        'temperature': temperature,
        'humidity': humidity,
        'rainfall': rainfall
    }

def generate_human_readable_explanation(features: Dict[str, float], crop: str, 
                                       feature_importance: Dict[str, float]) -> str:
    """
    Generate human-readable explanation for crop recommendation
    
    Args:
        features: Input feature values
        crop: Recommended crop
        feature_importance: Feature importance scores
        
    Returns:
        Human-readable explanation string
    """
    explanations = []
    
    # Get top 3 most important features
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)[:3]
    
    for feature_name, importance in sorted_features:
        value = features.get(feature_name, 0)
        explanation = _get_feature_explanation(feature_name, value, crop)
        if explanation:
            explanations.append(explanation)
    
    if explanations:
        return " ".join(explanations)
    else:
        return f"{crop} is suitable for the given soil and climate conditions."

def _get_feature_explanation(feature: str, value: float, crop: str) -> str:
    """Generate explanation for a single feature"""
    
    if feature == 'rainfall':
        if value > 200:
            return f"High rainfall ({value:.0f}mm) provides excellent moisture for {crop}."
        elif value > 100:
            return f"Moderate rainfall ({value:.0f}mm) is suitable for {crop}."
        else:
            return f"Low rainfall ({value:.0f}mm) matches {crop}'s water requirements."
    
    elif feature == 'humidity':
        if value > 80:
            return f"High humidity ({value:.0f}%) creates ideal conditions for {crop}."
        elif value > 60:
            return f"Moderate humidity ({value:.0f}%) supports {crop} growth."
        else:
            return f"Low humidity ({value:.0f}%) suits {crop}'s climate needs."
    
    elif feature == 'temperature':
        if value > 30:
            return f"Warm temperature ({value:.1f}°C) is optimal for {crop}."
        elif value > 20:
            return f"Moderate temperature ({value:.1f}°C) favors {crop} cultivation."
        else:
            return f"Cool temperature ({value:.1f}°C) is suitable for {crop}."
    
    elif feature == 'N':
        if value > 80:
            return f"High nitrogen content ({value:.0f}) supports vigorous {crop} growth."
        elif value > 40:
            return f"Moderate nitrogen ({value:.0f}) is adequate for {crop}."
        else:
            return f"Low nitrogen ({value:.0f}) matches {crop}'s nutrient needs."
    
    elif feature == 'P':
        if value > 60:
            return f"High phosphorus ({value:.0f}) promotes strong {crop} root development."
        else:
            return f"Phosphorus level ({value:.0f}) is suitable for {crop}."
    
    elif feature == 'K':
        if value > 40:
            return f"High potassium ({value:.0f}) enhances {crop} quality and disease resistance."
        else:
            return f"Potassium level ({value:.0f}) meets {crop}'s requirements."
    
    elif feature == 'pH':
        if 6.0 <= value <= 7.5:
            return f"Neutral pH ({value:.1f}) is ideal for {crop}."
        elif value < 6.0:
            return f"Acidic soil (pH {value:.1f}) suits {crop} well."
        else:
            return f"Alkaline soil (pH {value:.1f}) is appropriate for {crop}."
    
    return ""
