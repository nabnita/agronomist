"""
Sustainability analysis service
"""
from typing import Dict, Any, List
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

class SustainabilityService:
    """Service for analyzing crop sustainability and soil impact"""
    
    # Crop nutrient consumption rates (kg/ha per season)
    CROP_NPK_CONSUMPTION = {
        'rice': {'N': 120, 'P': 60, 'K': 60},
        'maize': {'N': 150, 'P': 75, 'K': 50},
        'chickpea': {'N': 20, 'P': 60, 'K': 40},  # Nitrogen-fixing
        'kidneybeans': {'N': 30, 'P': 50, 'K': 50},
        'pigeonpeas': {'N': 25, 'P': 50, 'K': 40},
        'mothbeans': {'N': 30, 'P': 45, 'K': 45},
        'mungbean': {'N': 25, 'P': 50, 'K': 50},
        'blackgram': {'N': 30, 'P': 50, 'K': 45},
        'lentil': {'N': 20, 'P': 55, 'K': 40},
        'pomegranate': {'N': 100, 'P': 50, 'K': 100},
        'banana': {'N': 200, 'P': 80, 'K': 200},
        'mango': {'N': 150, 'P': 100, 'K': 120},
        'grapes': {'N': 120, 'P': 80, 'K': 150},
        'watermelon': {'N': 100, 'P': 60, 'K': 80},
        'muskmelon': {'N': 90, 'P': 55, 'K': 75},
        'apple': {'N': 130, 'P': 90, 'K': 110},
        'orange': {'N': 140, 'P': 70, 'K': 100},
        'papaya': {'N': 110, 'P': 80, 'K': 90},
        'coconut': {'N': 100, 'P': 50, 'K': 120},
        'cotton': {'N': 120, 'P': 60, 'K': 60},
        'jute': {'N': 80, 'P': 40, 'K': 40},
        'coffee': {'N': 100, 'P': 50, 'K': 80}
    }
    
    # Water requirements (mm per season)
    CROP_WATER_NEEDS = {
        'rice': 1200, 'maize': 600, 'chickpea': 400, 'kidneybeans': 500,
        'pigeonpeas': 450, 'mothbeans': 400, 'mungbean': 350, 'blackgram': 400,
        'lentil': 450, 'pomegranate': 800, 'banana': 1500, 'mango': 1000,
        'grapes': 900, 'watermelon': 500, 'muskmelon': 450, 'apple': 800,
        'orange': 900, 'papaya': 800, 'coconut': 1200, 'cotton': 700,
        'jute': 600, 'coffee': 1000
    }
    
    def analyze_soil_impact(self, crop: str, soil_params: Dict[str, float], 
                           duration_months: int = 4) -> Dict[str, Any]:
        """
        Analyze sustainability impact of growing a crop
        
        Args:
            crop: Crop name
            soil_params: Current soil parameters (N, P, K, pH)
            duration_months: Growing duration in months
            
        Returns:
            Dictionary with sustainability analysis
        """
        crop_lower = crop.lower()
        
        # Calculate nutrient depletion
        depletion = self._calculate_nutrient_depletion(crop_lower, soil_params)
        
        # Calculate water risk
        water_risk = self._calculate_water_risk(crop_lower, soil_params.get('rainfall', 0))
        
        # Get crop rotation suggestions
        rotation = self._suggest_crop_rotation(crop_lower, depletion)
        
        # Calculate overall sustainability score
        sustainability_score = self._calculate_sustainability_score(
            depletion, water_risk, soil_params
        )
        
        return {
            'crop': crop,
            'sustainability_score': sustainability_score,
            'nutrient_depletion': depletion,
            'water_risk': water_risk,
            'crop_rotation': rotation,
            'recommendations': self._generate_recommendations(
                crop_lower, depletion, water_risk, sustainability_score
            )
        }
    
    def _calculate_nutrient_depletion(self, crop: str, soil_params: Dict[str, float]) -> Dict[str, Any]:
        """Calculate nutrient depletion estimates"""
        
        consumption = self.CROP_NPK_CONSUMPTION.get(crop, {'N': 100, 'P': 50, 'K': 50})
        
        current_n = soil_params.get('N', 50)
        current_p = soil_params.get('P', 50)
        current_k = soil_params.get('K', 50)
        
        # Calculate remaining nutrients after harvest
        remaining_n = max(0, current_n - consumption['N'])
        remaining_p = max(0, current_p - consumption['P'])
        remaining_k = max(0, current_k - consumption['K'])
        
        # Calculate depletion percentages
        n_depletion = (consumption['N'] / max(current_n, 1)) * 100
        p_depletion = (consumption['P'] / max(current_p, 1)) * 100
        k_depletion = (consumption['K'] / max(current_k, 1)) * 100
        
        return {
            'consumption': consumption,
            'remaining': {'N': remaining_n, 'P': remaining_p, 'K': remaining_k},
            'depletion_percent': {
                'N': min(100, n_depletion),
                'P': min(100, p_depletion),
                'K': min(100, k_depletion)
            },
            'severity': self._get_depletion_severity(n_depletion, p_depletion, k_depletion)
        }
    
    def _calculate_water_risk(self, crop: str, rainfall: float) -> Dict[str, Any]:
        """Calculate water usage risk"""
        
        water_need = self.CROP_WATER_NEEDS.get(crop, 600)
        
        # Assume rainfall is monthly average, multiply by 4 for season
        seasonal_rainfall = rainfall * 4
        
        water_deficit = max(0, water_need - seasonal_rainfall)
        water_surplus = max(0, seasonal_rainfall - water_need)
        
        # Calculate risk level
        if water_deficit > 400:
            risk_level = 'high'
            risk_message = f'Significant irrigation needed ({water_deficit:.0f}mm deficit)'
        elif water_deficit > 200:
            risk_level = 'medium'
            risk_message = f'Moderate irrigation required ({water_deficit:.0f}mm deficit)'
        elif water_surplus > 400:
            risk_level = 'medium'
            risk_message = f'Excess water may cause issues ({water_surplus:.0f}mm surplus)'
        else:
            risk_level = 'low'
            risk_message = 'Water availability is adequate'
        
        return {
            'water_need': water_need,
            'available_water': seasonal_rainfall,
            'deficit': water_deficit,
            'surplus': water_surplus,
            'risk_level': risk_level,
            'message': risk_message
        }
    
    def _suggest_crop_rotation(self, current_crop: str, depletion: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest crop rotation for soil recovery"""
        
        # Nitrogen-fixing crops for rotation
        nitrogen_fixers = ['chickpea', 'pigeonpeas', 'lentil', 'mungbean', 'blackgram']
        
        # Light feeders
        light_feeders = ['mothbeans', 'jute', 'watermelon', 'muskmelon']
        
        suggestions = []
        
        # If high nitrogen depletion, suggest nitrogen-fixing crops
        if depletion['depletion_percent']['N'] > 60:
            suggestions.append({
                'reason': 'High nitrogen depletion',
                'crops': nitrogen_fixers,
                'benefit': 'These crops will restore nitrogen to the soil'
            })
        
        # If overall high depletion, suggest light feeders
        avg_depletion = sum(depletion['depletion_percent'].values()) / 3
        if avg_depletion > 50:
            suggestions.append({
                'reason': 'Overall nutrient depletion',
                'crops': light_feeders,
                'benefit': 'These crops have lower nutrient requirements'
            })
        
        # Suggest fallow period if severe depletion
        if depletion['severity'] == 'severe':
            suggestions.append({
                'reason': 'Severe soil depletion',
                'crops': ['fallow period with cover crops'],
                'benefit': 'Allow soil to recover naturally'
            })
        
        return {
            'current_crop': current_crop,
            'suggestions': suggestions if suggestions else [{
                'reason': 'Soil health is good',
                'crops': ['Continue with similar crops or diversify'],
                'benefit': 'Maintain soil balance'
            }]
        }
    
    def _calculate_sustainability_score(self, depletion: Dict[str, Any], 
                                       water_risk: Dict[str, Any],
                                       soil_params: Dict[str, float]) -> int:
        """Calculate overall sustainability score (0-100)"""
        
        score = 100
        
        # Deduct for nutrient depletion
        avg_depletion = sum(depletion['depletion_percent'].values()) / 3
        score -= avg_depletion * 0.3
        
        # Deduct for water risk
        if water_risk['risk_level'] == 'high':
            score -= 20
        elif water_risk['risk_level'] == 'medium':
            score -= 10
        
        # Bonus for good pH
        pH = soil_params.get('pH', 7)
        if 6.0 <= pH <= 7.5:
            score += 5
        
        return max(0, min(100, int(score)))
    
    def _get_depletion_severity(self, n_dep: float, p_dep: float, k_dep: float) -> str:
        """Determine depletion severity level"""
        avg_depletion = (n_dep + p_dep + k_dep) / 3
        
        if avg_depletion > 70:
            return 'severe'
        elif avg_depletion > 50:
            return 'high'
        elif avg_depletion > 30:
            return 'moderate'
        else:
            return 'low'
    
    def _generate_recommendations(self, crop: str, depletion: Dict[str, Any],
                                 water_risk: Dict[str, Any], 
                                 score: int) -> List[str]:
        """Generate actionable sustainability recommendations"""
        
        recommendations = []
        
        # Nutrient recommendations
        if depletion['depletion_percent']['N'] > 50:
            recommendations.append('Apply nitrogen-rich fertilizers or compost before next planting')
        if depletion['depletion_percent']['P'] > 50:
            recommendations.append('Add phosphate fertilizers to restore phosphorus levels')
        if depletion['depletion_percent']['K'] > 50:
            recommendations.append('Use potash or wood ash to replenish potassium')
        
        # Water recommendations
        if water_risk['risk_level'] == 'high':
            recommendations.append('Install drip irrigation system to conserve water')
            recommendations.append('Use mulching to reduce water evaporation')
        elif water_risk['surplus'] > 300:
            recommendations.append('Ensure proper drainage to prevent waterlogging')
        
        # General sustainability
        if score < 60:
            recommendations.append('Consider crop rotation to improve soil health')
            recommendations.append('Add organic matter to enhance soil structure')
        
        if not recommendations:
            recommendations.append('Maintain current sustainable practices')
        
        return recommendations

# Singleton instance
_sustainability_service = None

def get_sustainability_service() -> SustainabilityService:
    """Get or create sustainability service singleton"""
    global _sustainability_service
    if _sustainability_service is None:
        _sustainability_service = SustainabilityService()
    return _sustainability_service
