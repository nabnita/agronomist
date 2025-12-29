"""
Configuration management for AgroMind AI
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask settings
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    PORT = int(os.getenv('PORT', 5000))
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    
    # Model paths
    BASE_DIR = Path(__file__).parent
    MODELS_DIR = BASE_DIR / 'models'
    DATA_DIR = BASE_DIR / 'data'
    
    MODEL_PATH = MODELS_DIR / 'crop_model.pkl'
    LABEL_ENCODER_PATH = MODELS_DIR / 'label_encoder.pkl'
    FEATURE_NAMES_PATH = MODELS_DIR / 'feature_names.pkl'
    
    # Dataset path
    DATASET_PATH = DATA_DIR / 'crop_data.csv'
    
    # Model parameters
    RANDOM_STATE = 42
    TEST_SIZE = 0.2
    N_ESTIMATORS = 100
    
    # Feature ranges for validation
    FEATURE_RANGES = {
        'N': (0, 140),
        'P': (5, 145),
        'K': (5, 205),
        'pH': (3.5, 9.5),
        'temperature': (8, 45),
        'humidity': (14, 100),
        'rainfall': (20, 300)
    }
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GEMINI_API_KEY and not cls.GROQ_API_KEY:
            print("⚠️  Warning: No AI API key configured. AI Agronomist feature will be disabled.")
        
        # Create directories if they don't exist
        cls.MODELS_DIR.mkdir(parents=True, exist_ok=True)
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        return True

# Validate configuration on import
Config.validate()
