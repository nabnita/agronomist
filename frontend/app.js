// AgroMind AI - Frontend Application Logic

// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// DOM Elements
const elements = {
    // Sliders
    nitrogenInput: document.getElementById('nitrogen-input'),
    phosphorusInput: document.getElementById('phosphorus-input'),
    potassiumInput: document.getElementById('potassium-input'),
    phInput: document.getElementById('ph-input'),
    temperatureInput: document.getElementById('temperature-input'),
    humidityInput: document.getElementById('humidity-input'),
    rainfallInput: document.getElementById('rainfall-input'),

    // Slider Values
    nitrogenValue: document.getElementById('nitrogen-value'),
    phosphorusValue: document.getElementById('phosphorus-value'),
    potassiumValue: document.getElementById('potassium-value'),
    phValue: document.getElementById('ph-value'),
    temperatureValue: document.getElementById('temperature-value'),
    humidityValue: document.getElementById('humidity-value'),
    rainfallValue: document.getElementById('rainfall-value'),

    // Buttons
    predictBtn: document.getElementById('predict-btn'),
    aiAdviceBtn: document.getElementById('ai-advice-btn'),

    // Sections
    resultsSection: document.getElementById('results-section'),
    cropCards: document.getElementById('crop-cards'),
    explanationSection: document.getElementById('explanation-section'),
    explanationContent: document.getElementById('explanation-content'),
    sustainabilitySection: document.getElementById('sustainability-section'),
    sustainabilityContent: document.getElementById('sustainability-content'),

    // AI Inputs
    cropNameInput: document.getElementById('crop-name-input'),
    locationInput: document.getElementById('location-input'),
    aiResponse: document.getElementById('ai-response'),

    // Loading
    loadingOverlay: document.getElementById('loading-overlay')
};

// State
let currentPredictions = [];
let currentInputs = {};

// Initialize
function init() {
    setupSliderListeners();
    setupButtonListeners();
    updateAllSliderValues();
}

// Parse markdown to HTML
function parseMarkdown(text) {
    if (!text) return '';

    // Convert markdown to HTML
    let html = text;

    // Headers (## Header)
    html = html.replace(/^### (.*$)/gim, '<h5>$1</h5>');
    html = html.replace(/^## (.*$)/gim, '<h4>$1</h4>');
    html = html.replace(/^# (.*$)/gim, '<h3>$1</h3>');

    // Bold (**text** or __text__)
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.+?)__/g, '<strong>$1</strong>');

    // Italic (*text* or _text_)
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    html = html.replace(/_(.+?)_/g, '<em>$1</em>');

    // Bullet lists (- item or * item)
    html = html.replace(/^\s*[-*]\s+(.+)$/gim, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>');

    // Numbered lists (1. item)
    html = html.replace(/^\s*\d+\.\s+(.+)$/gim, '<li>$1</li>');

    // Line breaks
    html = html.replace(/\n\n/g, '</p><p>');
    html = html.replace(/\n/g, '<br>');

    // Wrap in paragraph if not already wrapped
    if (!html.startsWith('<')) {
        html = '<p>' + html + '</p>';
    }

    return html;
}

// Setup slider event listeners
function setupSliderListeners() {
    const sliders = [
        { input: elements.nitrogenInput, value: elements.nitrogenValue, suffix: '' },
        { input: elements.phosphorusInput, value: elements.phosphorusValue, suffix: '' },
        { input: elements.potassiumInput, value: elements.potassiumValue, suffix: '' },
        { input: elements.phInput, value: elements.phValue, suffix: '' },
        { input: elements.temperatureInput, value: elements.temperatureValue, suffix: '°C' },
        { input: elements.humidityInput, value: elements.humidityValue, suffix: '%' },
        { input: elements.rainfallInput, value: elements.rainfallValue, suffix: 'mm' }
    ];

    sliders.forEach(({ input, value, suffix }) => {
        input.addEventListener('input', (e) => {
            value.textContent = e.target.value + suffix;
        });
    });
}

// Setup button listeners
function setupButtonListeners() {
    elements.predictBtn.addEventListener('click', handlePredict);
    elements.aiAdviceBtn.addEventListener('click', handleAIAdvice);
}

// Update all slider values on load
function updateAllSliderValues() {
    elements.nitrogenValue.textContent = elements.nitrogenInput.value;
    elements.phosphorusValue.textContent = elements.phosphorusInput.value;
    elements.potassiumValue.textContent = elements.potassiumInput.value;
    elements.phValue.textContent = elements.phInput.value;
    elements.temperatureValue.textContent = elements.temperatureInput.value + '°C';
    elements.humidityValue.textContent = elements.humidityInput.value + '%';
    elements.rainfallValue.textContent = elements.rainfallInput.value + 'mm';
}

// Get current input values
function getCurrentInputs() {
    return {
        N: parseFloat(elements.nitrogenInput.value),
        P: parseFloat(elements.phosphorusInput.value),
        K: parseFloat(elements.potassiumInput.value),
        pH: parseFloat(elements.phInput.value),
        temperature: parseFloat(elements.temperatureInput.value),
        humidity: parseFloat(elements.humidityInput.value),
        rainfall: parseFloat(elements.rainfallInput.value)
    };
}

// Show/Hide loading
function showLoading() {
    elements.loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    elements.loadingOverlay.classList.add('hidden');
}

// Handle Predict
async function handlePredict() {
    try {
        showLoading();

        currentInputs = getCurrentInputs();

        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentInputs)
        });

        const data = await response.json();

        if (data.success) {
            currentPredictions = data.predictions;
            displayPredictions(data.predictions);
            elements.resultsSection.classList.remove('hidden');

            // Scroll to results
            elements.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            alert('Error: ' + (data.error || 'Prediction failed'));
        }
    } catch (error) {
        console.error('Prediction error:', error);
        alert('Failed to get predictions. Make sure the backend server is running.');
    } finally {
        hideLoading();
    }
}

// Display predictions
function displayPredictions(predictions) {
    elements.cropCards.innerHTML = '';

    predictions.forEach((pred, index) => {
        const card = createCropCard(pred, index + 1);
        elements.cropCards.appendChild(card);
    });
}

// Create crop card
function createCropCard(prediction, rank) {
    const card = document.createElement('div');
    card.className = 'crop-card';

    const confidence = Math.round(prediction.confidence * 100);

    card.innerHTML = `
        <span class="crop-rank">#${rank} Recommendation</span>
        <h3 class="crop-name">${prediction.crop}</h3>
        <p class="confidence-label">Confidence Score</p>
        <div class="confidence-bar">
            <div class="confidence-fill" style="width: ${confidence}%"></div>
        </div>
        <p class="confidence-percent">${confidence}%</p>
        <button class="btn btn-explain" onclick="explainCrop('${prediction.crop}')">
            <span>📊 Why this crop?</span>
        </button>
        <button class="btn btn-explain" onclick="analyzeSustainability('${prediction.crop}')" style="margin-top: 0.5rem;">
            <span>🌍 Sustainability</span>
        </button>
    `;

    return card;
}

// Explain crop (global function for onclick)
window.explainCrop = async function (crop) {
    try {
        showLoading();

        const requestData = {
            ...currentInputs,
            crop: crop
        };

        const response = await fetch(`${API_BASE_URL}/explain`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (data.success) {
            displayExplanation(data.explanation);
            elements.explanationSection.classList.remove('hidden');
            elements.explanationSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            alert('Error: ' + (data.error || 'Explanation failed'));
        }
    } catch (error) {
        console.error('Explanation error:', error);
        alert('Failed to get explanation. Make sure the backend server is running.');
    } finally {
        hideLoading();
    }
};

// Display explanation
function displayExplanation(explanation) {
    elements.explanationContent.innerHTML = `
        <h3 style="color: var(--secondary-green); margin-bottom: 1rem; text-transform: capitalize;">
            ${explanation.crop}
        </h3>
        <div class="explanation-text">
            <p>${explanation.explanation}</p>
        </div>
        
        <div class="feature-importance">
            <h4 style="margin-bottom: 1rem;">Feature Importance</h4>
            ${explanation.importance_chart.map(item => `
                <div class="feature-item">
                    <span class="feature-name">${item.feature}</span>
                    <div class="feature-bar">
                        <div class="feature-fill" style="width: ${item.importance * 100}%">
                            <span class="feature-value">${item.importance_percent}</span>
                        </div>
                    </div>
                </div>
            `).join('')}
        </div>
    `;
}

// Analyze sustainability (global function for onclick)
window.analyzeSustainability = async function (crop) {
    try {
        showLoading();

        const requestData = {
            crop: crop,
            N: currentInputs.N,
            P: currentInputs.P,
            K: currentInputs.K,
            pH: currentInputs.pH,
            rainfall: currentInputs.rainfall
        };

        const response = await fetch(`${API_BASE_URL}/soil-impact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (data.success) {
            displaySustainability(data.analysis);
            elements.sustainabilitySection.classList.remove('hidden');
            elements.sustainabilitySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        } else {
            alert('Error: ' + (data.error || 'Sustainability analysis failed'));
        }
    } catch (error) {
        console.error('Sustainability error:', error);
        alert('Failed to get sustainability analysis. Make sure the backend server is running.');
    } finally {
        hideLoading();
    }
};

// Display sustainability analysis
function displaySustainability(analysis) {
    const score = analysis.sustainability_score;
    const scoreRotation = (score / 100) * 360;

    elements.sustainabilityContent.innerHTML = `
        <h3 style="color: var(--secondary-green); margin-bottom: 1rem; text-transform: capitalize;">
            ${analysis.crop} - Sustainability Analysis
        </h3>
        
        <div class="sustainability-score">
            <div class="score-circle" style="background: conic-gradient(var(--accent-green) ${scoreRotation}deg, var(--cream-dark) ${scoreRotation}deg);">
                <div class="score-inner">
                    <div class="score-number">${score}</div>
                    <div class="score-label">Score</div>
                </div>
            </div>
            <p style="color: var(--text-medium);">
                ${score >= 70 ? 'Excellent' : score >= 50 ? 'Good' : 'Needs Attention'} Sustainability
            </p>
        </div>
        
        <div class="sustainability-grid">
            <div class="sustainability-card">
                <h4>Nutrient Depletion</h4>
                <div class="depletion-item">
                    <span>Nitrogen (N)</span>
                    <strong style="color: ${getDepletionColor(analysis.nutrient_depletion.depletion_percent.N)}">
                        ${Math.round(analysis.nutrient_depletion.depletion_percent.N)}%
                    </strong>
                </div>
                <div class="depletion-item">
                    <span>Phosphorus (P)</span>
                    <strong style="color: ${getDepletionColor(analysis.nutrient_depletion.depletion_percent.P)}">
                        ${Math.round(analysis.nutrient_depletion.depletion_percent.P)}%
                    </strong>
                </div>
                <div class="depletion-item">
                    <span>Potassium (K)</span>
                    <strong style="color: ${getDepletionColor(analysis.nutrient_depletion.depletion_percent.K)}">
                        ${Math.round(analysis.nutrient_depletion.depletion_percent.K)}%
                    </strong>
                </div>
            </div>
            
            <div class="sustainability-card">
                <h4>Water Risk</h4>
                <p><strong>Level:</strong> ${analysis.water_risk.risk_level.toUpperCase()}</p>
                <p>${analysis.water_risk.message}</p>
                <p style="margin-top: 0.5rem;">
                    <strong>Water Need:</strong> ${analysis.water_risk.water_need}mm<br>
                    <strong>Available:</strong> ${Math.round(analysis.water_risk.available_water)}mm
                </p>
            </div>
        </div>
        
        <div class="sustainability-card">
            <h4>Recommendations</h4>
            <ul class="recommendations-list">
                ${analysis.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
        </div>
        
        ${analysis.crop_rotation.suggestions.length > 0 ? `
            <div class="sustainability-card">
                <h4>Crop Rotation Suggestions</h4>
                ${analysis.crop_rotation.suggestions.map(sug => `
                    <div style="margin-bottom: 1rem;">
                        <p><strong>${sug.reason}</strong></p>
                        <p style="color: var(--text-medium);">${sug.benefit}</p>
                        <p style="margin-top: 0.5rem;">
                            <em>Suggested crops: ${Array.isArray(sug.crops) ? sug.crops.join(', ') : sug.crops}</em>
                        </p>
                    </div>
                `).join('')}
            </div>
        ` : ''}
    `;
}

// Get depletion color
function getDepletionColor(percent) {
    if (percent > 70) return '#d32f2f';
    if (percent > 50) return '#f57c00';
    if (percent > 30) return '#fbc02d';
    return '#388e3c';
}

// Handle AI Advice
async function handleAIAdvice() {
    try {
        const cropName = elements.cropNameInput.value.trim();
        const location = elements.locationInput.value.trim();

        if (!cropName) {
            alert('Please enter a crop name');
            return;
        }

        showLoading();

        const requestData = {
            crop: cropName,
            ...getCurrentInputs(),
            location: location || undefined
        };

        const response = await fetch(`${API_BASE_URL}/ai-advice`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (data.success) {
            displayAIAdvice(data);
            elements.aiResponse.classList.remove('hidden');
        } else {
            alert('Error: ' + (data.error || 'AI advice failed. Make sure you have configured your Gemini API key.'));
        }
    } catch (error) {
        console.error('AI advice error:', error);
        alert('Failed to get AI advice. Make sure the backend server is running and API key is configured.');
    } finally {
        hideLoading();
    }
}

// Display AI advice with enhanced formatting
function displayAIAdvice(data) {
    const advice = data.advice;

    let html = `
        <div class="ai-advice-header">
            <h3 style="color: var(--secondary-green); text-transform: capitalize; display: flex; align-items: center; gap: 0.5rem;">
                <span>🌾</span>
                <span>AI Farming Advice for ${data.crop}</span>
            </h3>
        </div>
    `;

    // Suitability Assessment
    if (advice.suitability) {
        html += `
            <div class="advice-section">
                <h4><span class="advice-icon">✅</span> Suitability Assessment</h4>
                <div class="advice-content">${parseMarkdown(advice.suitability)}</div>
            </div>
        `;
    }

    // Best Sowing Season
    if (advice.sowing_season) {
        html += `
            <div class="advice-section">
                <h4><span class="advice-icon">📅</span> Best Sowing Season</h4>
                <div class="advice-content">${parseMarkdown(advice.sowing_season)}</div>
            </div>
        `;
    }

    // Fertilizer Recommendations
    if (advice.fertilizer) {
        html += `
            <div class="advice-section">
                <h4><span class="advice-icon">🧪</span> Fertilizer Recommendations</h4>
                <div class="advice-content">${parseMarkdown(advice.fertilizer)}</div>
            </div>
        `;
    }

    // Disease & Pest Risks
    if (advice.disease_risks) {
        html += `
            <div class="advice-section">
                <h4><span class="advice-icon">🐛</span> Disease & Pest Risks</h4>
                <div class="advice-content">${parseMarkdown(advice.disease_risks)}</div>
            </div>
        `;
    }

    // Yield Optimization Tips
    if (advice.yield_tips) {
        html += `
            <div class="advice-section">
                <h4><span class="advice-icon">📈</span> Yield Optimization Tips</h4>
                <div class="advice-content">${parseMarkdown(advice.yield_tips)}</div>
            </div>
        `;
    }

    // Fallback to full text if sections not parsed
    if (!advice.suitability && !advice.sowing_season && advice.full_text) {
        html += `
            <div class="advice-section">
                <div class="advice-content">${parseMarkdown(advice.full_text)}</div>
            </div>
        `;
    }

    elements.aiResponse.innerHTML = html;
}

// Initialize on load
document.addEventListener('DOMContentLoaded', init);
