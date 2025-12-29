"""
Train RandomForest model for crop recommendation
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.config import Config

def load_data():
    """Load crop dataset"""
    print("📊 Loading dataset...")
    # Use custom dataset from dataset folder
    dataset_path = Path(__file__).parent.parent / 'dataset' / 'Crop_recommendation.csv'
    df = pd.read_csv(dataset_path)
    
    # Rename 'label' column to 'crop' for consistency
    if 'label' in df.columns:
        df = df.rename(columns={'label': 'crop'})
    
    print(f"✓ Loaded {len(df)} samples with {len(df['crop'].unique())} crop types")
    return df


def preprocess_data(df):
    """Preprocess data for training"""
    print("\n🔧 Preprocessing data...")
    
    # Separate features and target
    X = df.drop('crop', axis=1)
    y = df['crop']
    
    # Encode crop labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Get feature names
    feature_names = X.columns.tolist()
    
    print(f"✓ Features: {', '.join(feature_names)}")
    print(f"✓ Crops: {', '.join(label_encoder.classes_)}")
    
    return X, y_encoded, label_encoder, feature_names

def train_model(X, y):
    """Train RandomForest classifier"""
    print("\n🤖 Training RandomForest model...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=Config.TEST_SIZE, 
        random_state=Config.RANDOM_STATE,
        stratify=y
    )
    
    print(f"✓ Training set: {len(X_train)} samples")
    print(f"✓ Test set: {len(X_test)} samples")
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=Config.N_ESTIMATORS,
        random_state=Config.RANDOM_STATE,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        n_jobs=-1
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\n✅ Model trained successfully!")
    print(f"✓ Accuracy: {accuracy * 100:.2f}%")
    
    return model, X_test, y_test, y_pred

def evaluate_model(model, X_test, y_test, y_pred, label_encoder):
    """Detailed model evaluation"""
    print("\n📈 Model Evaluation:")
    print("=" * 60)
    
    # Overall metrics
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Overall Accuracy: {accuracy * 100:.2f}%")
    
    # Per-crop report
    print("\nPer-Crop Performance:")
    print(classification_report(
        y_test, y_pred, 
        target_names=label_encoder.classes_,
        zero_division=0
    ))
    
    # Feature importance
    feature_importance = model.feature_importances_
    print("\nFeature Importance:")
    for i, importance in enumerate(feature_importance):
        feature_name = ['N', 'P', 'K', 'pH', 'temperature', 'humidity', 'rainfall'][i]
        print(f"  {feature_name:12s}: {importance:.4f} {'█' * int(importance * 50)}")

def save_model(model, label_encoder, feature_names):
    """Save trained model and encoders"""
    print("\n💾 Saving model...")
    
    # Ensure models directory exists
    Config.MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save model
    joblib.dump(model, Config.MODEL_PATH)
    print(f"✓ Model saved to: {Config.MODEL_PATH}")
    
    # Save label encoder
    joblib.dump(label_encoder, Config.LABEL_ENCODER_PATH)
    print(f"✓ Label encoder saved to: {Config.LABEL_ENCODER_PATH}")
    
    # Save feature names
    joblib.dump(feature_names, Config.FEATURE_NAMES_PATH)
    print(f"✓ Feature names saved to: {Config.FEATURE_NAMES_PATH}")

def main():
    """Main training pipeline"""
    print("🌱 AgroMind AI - Model Training")
    print("=" * 60)
    
    # Load data
    df = load_data()
    
    # Preprocess
    X, y, label_encoder, feature_names = preprocess_data(df)
    
    # Train
    model, X_test, y_test, y_pred = train_model(X, y)
    
    # Evaluate
    evaluate_model(model, X_test, y_test, y_pred, label_encoder)
    
    # Save
    save_model(model, label_encoder, feature_names)
    
    print("\n" + "=" * 60)
    print("🎉 Training complete! Model ready for deployment.")
    print("=" * 60)

if __name__ == "__main__":
    main()
