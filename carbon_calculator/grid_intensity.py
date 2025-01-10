"""
Grid intensity data by country.
"""
import json
from urllib import request
from typing import Dict, Optional

class GridIntensity:
    def __init__(self):
        # Cache for grid intensity data
        self._intensity_data = None
        
    def _load_intensity_data(self) -> None:
        if self._intensity_data is None:
            try:
                url = "https://ember-climate.org/api/data-catalogue/yearly-electricity-data"
                with request.urlopen(url) as response:
                    data = json.loads(response.read())
                    self._intensity_data = self._process_ember_data(data)
            except Exception:
                # Fallback to world average if API fails
                self._intensity_data = {'WORLD': 475} 
    
    def _process_ember_data(self, data: Dict) -> Dict[str, float]:
        """Process Ember data into country-specific grid intensities."""
        processed = {}
        for entry in data:
            if 'carbon_intensity' in entry:
                processed[entry['country_code']] = float(entry['carbon_intensity'])
        return processed
    
    def get_intensity(self, country_code: str = 'WORLD') -> float:
        """
        Get grid intensity for a country in gCO2/kWh.
        
        Args:
            country_code: ISO 3166-1 alpha-2 country code
            
        Returns:
            Grid intensity in gCO2/kWh
        """
        self._load_intensity_data()
        return self._intensity_data.get(country_code.upper(), self._intensity_data['WORLD'])