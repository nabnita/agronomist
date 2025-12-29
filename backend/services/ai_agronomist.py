"""
AI Agronomist service using Gemini API
"""
import os
from typing import Dict, Any, Optional
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from config import Config

# Try to import Gemini
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️  google-generativeai not installed. AI Agronomist will be disabled.")

class AIAgronomist:
    """AI-powered agricultural advisor using Gemini"""
    
    def __init__(self):
        """Initialize AI Agronomist"""
        self.model = None
        self.api_key = Config.GEMINI_API_KEY
        
        if self.api_key and GEMINI_AVAILABLE:
            self._initialize_gemini()
        else:
            print("⚠️  Gemini API key not configured. AI Agronomist disabled.")
    
    def _initialize_gemini(self):
        """Initialize Gemini API with Gemini 2.5 Flash"""
        try:
            genai.configure(api_key=self.api_key)
            # Use Gemini 2.5 Flash model
            self.model = genai.GenerativeModel('gemini-2.5-flash')
            print("✓ Gemini 2.5 Flash AI Agronomist initialized successfully")
        except Exception as e:
            print(f"⚠️  Gemini initialization error: {e}")
            self.model = None
    
    def get_farming_advice(self, crop: str, soil_params: Dict[str, float], 
                          climate_params: Dict[str, float], 
                          location: Optional[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive farming advice for a crop
        
        Args:
            crop: Crop name
            soil_params: Dict with N, P, K, pH
            climate_params: Dict with temperature, humidity, rainfall
            location: Optional location for region-specific advice
            
        Returns:
            Dictionary with farming advice
        """
        if not self.model:
            return {
                'success': False,
                'error': 'AI Agronomist not available. Please configure GEMINI_API_KEY.'
            }
        
        try:
            # Build prompt
            prompt = self._build_prompt(crop, soil_params, climate_params, location)
            
            # Generate response
            response = self.model.generate_content(prompt)
            
            # Parse and format response
            advice = self._parse_response(response.text)
            
            return {
                'success': True,
                'crop': crop,
                'advice': advice,
                'raw_response': response.text
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': f'AI Agronomist error: {str(e)}'
            }
    
    def _build_prompt(self, crop: str, soil_params: Dict[str, float], 
                     climate_params: Dict[str, float], 
                     location: Optional[str]) -> str:
        """Build comprehensive prompt for AI agronomist"""
        
        location_text = f" in {location}" if location else ""
        
        prompt = f"""You are an expert agricultural advisor helping farmers grow {crop}{location_text}.

**Soil Conditions:**
- Nitrogen (N): {soil_params.get('N', 'N/A')} kg/ha
- Phosphorus (P): {soil_params.get('P', 'N/A')} kg/ha
- Potassium (K): {soil_params.get('K', 'N/A')} kg/ha
- pH Level: {soil_params.get('pH', 'N/A')}

**Climate Conditions:**
- Temperature: {climate_params.get('temperature', 'N/A')}°C
- Humidity: {climate_params.get('humidity', 'N/A')}%
- Rainfall: {climate_params.get('rainfall', 'N/A')}mm

Please provide practical, farmer-friendly advice covering:

1. **Suitability Assessment**: Is this crop suitable for these conditions? (2-3 sentences)

2. **Best Sowing Season**: When to plant for optimal yield (1-2 sentences)

3. **Fertilizer Recommendations**: Specific NPK adjustments needed (2-3 sentences)

4. **Disease & Pest Risks**: Common issues to watch for (2-3 sentences)

5. **Yield Optimization Tips**: 3-4 actionable tips to maximize harvest

Keep language simple and practical. Avoid overly technical jargon. Focus on actionable advice."""

        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """Parse AI response into structured sections with improved detection"""
        
        sections = {
            'suitability': '',
            'sowing_season': '',
            'fertilizer': '',
            'disease_risks': '',
            'yield_tips': '',
            'full_text': response_text
        }
        
        # Split by lines and process
        lines = response_text.split('\n')
        current_section = None
        section_content = []
        
        for line in lines:
            line_stripped = line.strip()
            if not line_stripped:
                continue
                
            line_lower = line_stripped.lower()
            
            # Detect section headers (with various formats)
            if any(keyword in line_lower for keyword in ['suitability', 'suitable for']):
                if current_section and section_content:
                    sections[current_section] = ' '.join(section_content)
                current_section = 'suitability'
                section_content = []
                # Include content after header if on same line
                if ':' in line_stripped:
                    content = line_stripped.split(':', 1)[1].strip()
                    if content and not content.startswith('*'):
                        section_content.append(content)
            elif any(keyword in line_lower for keyword in ['sowing', 'planting', 'season']):
                if current_section and section_content:
                    sections[current_section] = ' '.join(section_content)
                current_section = 'sowing_season'
                section_content = []
                if ':' in line_stripped:
                    content = line_stripped.split(':', 1)[1].strip()
                    if content and not content.startswith('*'):
                        section_content.append(content)
            elif any(keyword in line_lower for keyword in ['fertilizer', 'npk', 'nutrient']):
                if current_section and section_content:
                    sections[current_section] = ' '.join(section_content)
                current_section = 'fertilizer'
                section_content = []
                if ':' in line_stripped:
                    content = line_stripped.split(':', 1)[1].strip()
                    if content and not content.startswith('*'):
                        section_content.append(content)
            elif any(keyword in line_lower for keyword in ['disease', 'pest', 'risk']):
                if current_section and section_content:
                    sections[current_section] = ' '.join(section_content)
                current_section = 'disease_risks'
                section_content = []
                if ':' in line_stripped:
                    content = line_stripped.split(':', 1)[1].strip()
                    if content and not content.startswith('*'):
                        section_content.append(content)
            elif any(keyword in line_lower for keyword in ['yield', 'optimization', 'tips', 'maximize']):
                if current_section and section_content:
                    sections[current_section] = ' '.join(section_content)
                current_section = 'yield_tips'
                section_content = []
                if ':' in line_stripped:
                    content = line_stripped.split(':', 1)[1].strip()
                    if content and not content.startswith('*'):
                        section_content.append(content)
            elif current_section:
                # Add content to current section, handling bullet points
                if line_stripped.startswith(('*', '-', '•', '1.', '2.', '3.', '4.', '5.')):
                    # Clean up bullet point
                    content = line_stripped.lstrip('*-•0123456789. ').strip()
                    if content:
                        section_content.append(content)
                elif not line_stripped.startswith('#'):  # Skip markdown headers
                    section_content.append(line_stripped)
        
        # Save last section
        if current_section and section_content:
            sections[current_section] = ' '.join(section_content)
        
        # Clean up sections - remove extra spaces and format
        for key in sections:
            if key != 'full_text':
                sections[key] = sections[key].strip()
                # Remove multiple spaces
                sections[key] = ' '.join(sections[key].split())
        
        return sections

# Singleton instance
_ai_agronomist = None

def get_ai_agronomist() -> AIAgronomist:
    """Get or create AI agronomist singleton"""
    global _ai_agronomist
    if _ai_agronomist is None:
        _ai_agronomist = AIAgronomist()
    return _ai_agronomist
