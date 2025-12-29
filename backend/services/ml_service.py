"""
Machine Learning service for crop prediction
"""
import numpy as np
import joblib
from typing import List, Dict, Any
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import Config
from utils.helpers import get_top_n_predictions

class MLService:
    """Machine Learning prediction service"""
    
    def __init__(self):
        """Initialize ML service and load model"""
        self.model = None
        self.label_encoder = None
        self.feature_names = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and encoders"""
        try:
            self.model = joblib.load(Config.MODEL_PATH)
            self.label_encoder = joblib.load(Config.LABEL_ENCODER_PATH)
            self.feature_names = joblib.load(Config.FEATURE_NAMES_PATH)
            print("✓ ML model loaded successfully")
        except FileNotFoundError as e:
            print(f"⚠️  Model not found. Please train the model first using: python scripts/train_model.py")
            raise e
    
    def predict_top_crops(self, features: Dict[str, float], n: int = 3) -> List[Dict[str, Any]]:
        """
        Predict top N crops with confidence scores
        
        Args:
            features: Dictionary with N, P, K, pH, temperature, humidity, rainfall
            n: Number of top predictions to return
            
        Returns:
            List of dicts with crop name and confidence scores
        """
        # Prepare feature array in correct order
        feature_array = np.array([[
            features['N'],
            features['P'],
            features['K'],
            features['pH'],
            features['temperature'],
            features['humidity'],
            features['rainfall']
        ]])
        
        # Get probabilities for all classes
        probabilities = self.model.predict_proba(feature_array)[0]
        
        # Get crop labels
        crop_labels = self.label_encoder.classes_.tolist()
        
        # Get top N predictions
        top_predictions = get_top_n_predictions(probabilities, crop_labels, n)
        
        return top_predictions
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from the model
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        importance_scores = self.model.feature_importances_
        
        return {
            feature: float(score) 
            for feature, score in zip(self.feature_names, importance_scores)
        }
    
    def get_all_crops(self) -> List[str]:
        """
        Get list of all crops the model can predict
        
        Returns:
            List of crop names
        """
        return self.label_encoder.classes_.tolist()

# Singleton instance
_ml_service = None

def get_ml_service() -> MLService:
    """Get or create ML service singleton"""
    global _ml_service
    if _ml_service is None:
        _ml_service = MLService()
    return _ml_service
