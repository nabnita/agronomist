"""
Explainable AI service using SHAP and feature importance
"""
import numpy as np
import shap
from typing import Dict, Any, List
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from services.ml_service import get_ml_service
from utils.helpers import generate_human_readable_explanation

class ExplainerService:
    """Service for generating explanations for predictions"""
    
    def __init__(self):
        """Initialize explainer service"""
        self.ml_service = get_ml_service()
        self.explainer = None
        self._initialize_shap()
    
    def _initialize_shap(self):
        """Initialize SHAP explainer"""
        try:
            # Use TreeExplainer for RandomForest
            self.explainer = shap.TreeExplainer(self.ml_service.model)
            print("✓ SHAP explainer initialized")
        except Exception as e:
            print(f"⚠️  SHAP initialization warning: {e}")
            self.explainer = None
    
    def explain_prediction(self, features: Dict[str, float], crop: str) -> Dict[str, Any]:
        """
        Generate comprehensive explanation for a crop prediction
        
        Args:
            features: Input features (N, P, K, pH, temperature, humidity, rainfall)
            crop: Crop to explain
            
        Returns:
            Dictionary with feature importance, SHAP values, and human explanation
        """
        # Get feature importance
        feature_importance = self.ml_service.get_feature_importance()
        
        # Get SHAP values if available
        shap_values = None
        if self.explainer:
            shap_values = self._get_shap_values(features, crop)
        
        # Generate human-readable explanation
        human_explanation = generate_human_readable_explanation(
            features, crop, feature_importance
        )
        
        # Prepare visualization data
        importance_chart_data = self._prepare_importance_chart(feature_importance)
        
        return {
            'crop': crop,
            'explanation': human_explanation,
            'feature_importance': feature_importance,
            'importance_chart': importance_chart_data,
            'shap_values': shap_values,
            'features': features
        }
    
    def _get_shap_values(self, features: Dict[str, float], crop: str) -> Dict[str, Any]:
        """Calculate SHAP values for the prediction"""
        try:
            # Prepare feature array
            feature_array = np.array([[
                features['N'],
                features['P'],
                features['K'],
                features['pH'],
                features['temperature'],
                features['humidity'],
                features['rainfall']
            ]])
            
            # Calculate SHAP values
            shap_vals = self.explainer.shap_values(feature_array)
            
            # Get crop index
            all_crops = self.ml_service.get_all_crops()
            crop_idx = all_crops.index(crop)
            
            # Extract SHAP values for this crop
            crop_shap_values = shap_vals[crop_idx][0] if isinstance(shap_vals, list) else shap_vals[0]
            
            # Create feature-to-shap mapping
            shap_dict = {
                feature: float(shap_val)
                for feature, shap_val in zip(self.ml_service.feature_names, crop_shap_values)
            }
            
            return {
                'values': shap_dict,
                'base_value': float(self.explainer.expected_value[crop_idx]) if isinstance(self.explainer.expected_value, np.ndarray) else float(self.explainer.expected_value)
            }
        except Exception as e:
            print(f"⚠️  SHAP calculation error: {e}")
            return None
    
    def _prepare_importance_chart(self, feature_importance: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Prepare feature importance data for frontend chart
        
        Args:
            feature_importance: Dictionary of feature importance scores
            
        Returns:
            List of dicts with feature and importance for charting
        """
        # Sort by importance
        sorted_features = sorted(
            feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {
                'feature': feature,
                'importance': importance,
                'importance_percent': f"{importance * 100:.1f}%"
            }
            for feature, importance in sorted_features
        ]
    
    def get_global_feature_importance(self) -> Dict[str, Any]:
        """
        Get global feature importance across all predictions
        
        Returns:
            Dictionary with feature importance data
        """
        feature_importance = self.ml_service.get_feature_importance()
        chart_data = self._prepare_importance_chart(feature_importance)
        
        return {
            'feature_importance': feature_importance,
            'chart_data': chart_data
        }

# Singleton instance
_explainer_service = None

def get_explainer_service() -> ExplainerService:
    """Get or create explainer service singleton"""
    global _explainer_service
    if _explainer_service is None:
        _explainer_service = ExplainerService()
    return _explainer_service
