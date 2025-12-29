"""
Input validation utilities for AgroMind AI
"""
from typing import Dict, Tuple, Any
from config import Config

class ValidationError(Exception):
    """Custom validation error"""
    pass

def validate_soil_climate_input(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate soil and climate input parameters
    
    Args:
        data: Dictionary with N, P, K, pH, temperature, humidity, rainfall
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = ['N', 'P', 'K', 'pH', 'temperature', 'humidity', 'rainfall']
    
    # Check all required fields present
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # Validate each field is numeric and within range
    for field in required_fields:
        value = data[field]
        
        # Check if numeric
        try:
            value = float(value)
        except (ValueError, TypeError):
            return False, f"Field '{field}' must be a number, got: {value}"
        
        # Check range
        if field in Config.FEATURE_RANGES:
            min_val, max_val = Config.FEATURE_RANGES[field]
            if not (min_val <= value <= max_val):
                return False, f"Field '{field}' must be between {min_val} and {max_val}, got: {value}"
    
    return True, ""

def validate_crop_name(crop: str, valid_crops: list) -> Tuple[bool, str]:
    """
    Validate crop name against known crops
    
    Args:
        crop: Crop name to validate
        valid_crops: List of valid crop names
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not crop:
        return False, "Crop name is required"
    
    if crop not in valid_crops:
        return False, f"Unknown crop: {crop}. Valid crops: {', '.join(valid_crops[:10])}..."
    
    return True, ""

def sanitize_input(data: Dict[str, Any]) -> Dict[str, float]:
    """
    Sanitize and convert input data to proper types
    
    Args:
        data: Raw input data
        
    Returns:
        Sanitized data with float values
    """
    sanitized = {}
    for key, value in data.items():
        try:
            sanitized[key] = float(value)
        except (ValueError, TypeError):
            sanitized[key] = value
    
    return sanitized
