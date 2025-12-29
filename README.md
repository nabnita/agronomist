# 🌱 AgroMind AI - Smart Crop Recommendation System

A production-ready crop recommendation system powered by Machine Learning, Explainable AI, and AI-powered agricultural advisory.

## ✨ Features

- **🤖 ML-Powered Predictions**: RandomForest classifier for accurate crop recommendations
- **📊 Top-3 Recommendations**: Get the best 3 crops with confidence scores
- **🔍 Explainable AI**: SHAP values and human-readable explanations
- **💡 AI Agronomist**: Gemini-powered farming advice and expert guidance
- **🌍 Sustainability Analysis**: Soil depletion, water risk, and crop rotation suggestions
- **🎨 Modern UI**: Beautiful agricultural-themed interface with glassmorphism
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## 🏗️ Architecture

```
crop recommendation/
├── backend/               # Flask API server
│   ├── app.py            # Main application
│   ├── config.py         # Configuration
│   ├── services/         # Business logic
│   │   ├── ml_service.py
│   │   ├── explainer_service.py
│   │   ├── ai_agronomist.py
│   │   └── sustainability_service.py
│   ├── routes/           # API endpoints
│   ├── utils/            # Helpers and validators
│   ├── models/           # Trained ML models
│   └── data/             # Training dataset
├── frontend/             # Web interface
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── scripts/              # Utility scripts
    └── train_model.py    # Model training
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip
- Gemini API key (for AI Agronomist feature)

### Installation

1. **Clone or navigate to the project directory**

2. **Install Python dependencies**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure API Key**

Create a `.env` file in the root directory:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_actual_api_key_here
```

4. **Train the ML Model**
```bash
python scripts/train_model.py
```

This will:
- Load the crop dataset
- Train a RandomForest classifier
- Save the model to `backend/models/`
- Display accuracy metrics

5. **Start the Backend Server**
```bash
cd backend
python app.py
```

Server will start at `http://localhost:5000`

6. **Open the Frontend**

Open `frontend/index.html` in your browser, or use a local server:
```bash
# Using Python
cd frontend
python -m http.server 5500

# Then open http://localhost:5500
```

## 📡 API Endpoints

### POST /api/predict
Get top-3 crop recommendations

**Request:**
```json
{
  "N": 90,
  "P": 42,
  "K": 43,
  "pH": 6.5,
  "temperature": 20.8,
  "humidity": 82,
  "rainfall": 202
}
```

**Response:**
```json
{
  "success": true,
  "predictions": [
    {
      "crop": "rice",
      "confidence": 0.95,
      "confidence_percent": "95.0%"
    }
  ]
}
```

### POST /api/explain
Get explanation for a crop recommendation

**Request:**
```json
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
```

### POST /api/ai-advice
Get AI-powered farming advice

**Request:**
```json
{
  "crop": "rice",
  "N": 90,
  "P": 42,
  "K": 43,
  "pH": 6.5,
  "temperature": 20.8,
  "humidity": 82,
  "rainfall": 202,
  "location": "Punjab"
}
```

### POST /api/soil-impact
Analyze sustainability and soil impact

**Request:**
```json
{
  "crop": "rice",
  "N": 90,
  "P": 42,
  "K": 43,
  "pH": 6.5,
  "rainfall": 202
}
```

### GET /api/crops
Get list of all available crops

### GET /api/health
Health check endpoint

## 🎯 Usage Guide

1. **Adjust Soil Parameters**: Use sliders to set N, P, K, and pH levels
2. **Set Climate Conditions**: Configure temperature, humidity, and rainfall
3. **Get Recommendations**: Click "Get Crop Recommendations"
4. **View Results**: See top-3 crops with confidence scores
5. **Explore Explanations**: Click "Why this crop?" for detailed insights
6. **Check Sustainability**: Click "Sustainability" for soil impact analysis
7. **Ask AI Agronomist**: Enter crop name for expert farming advice

## 🧪 Technology Stack

### Backend
- **Flask**: Web framework
- **scikit-learn**: Machine learning
- **SHAP**: Explainable AI
- **Gemini API**: AI agronomist
- **pandas/numpy**: Data processing

### Frontend
- **HTML5**: Semantic structure
- **CSS3**: Modern styling with glassmorphism
- **Vanilla JavaScript**: No framework dependencies
- **Google Fonts**: Outfit & Inter typography

## 📊 Model Performance

The RandomForest classifier achieves:
- **Accuracy**: >95% on test set
- **Features**: 7 input parameters (N, P, K, pH, temperature, humidity, rainfall)
- **Crops**: 22 different crop types
- **Training**: Stratified split for balanced evaluation

## 🌱 Supported Crops

rice, maize, chickpea, kidneybeans, pigeonpeas, mothbeans, mungbean, blackgram, lentil, pomegranate, banana, mango, grapes, watermelon, muskmelon, apple, orange, papaya, coconut, cotton, jute, coffee

## 🔧 Configuration

Edit `backend/config.py` to customize:
- Model parameters
- Feature ranges
- API settings
- File paths

## 🐛 Troubleshooting

**Model not found error:**
```bash
python scripts/train_model.py
```

**CORS errors:**
- Ensure backend is running on port 5000
- Check CORS_ORIGINS in `.env`

**AI Agronomist not working:**
- Verify Gemini API key in `.env`
- Check API quota and limits

**Port already in use:**
- Change PORT in `.env`
- Or kill the process using port 5000

## 📝 License

This project is for educational and agricultural development purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📧 Support

For issues and questions, please open a GitHub issue.

---

**Built with ❤️ for sustainable farming and AI-powered agriculture**
