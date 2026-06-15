"""
Grid intensity data by country.
"""
import json
import os
from urllib import parse
from urllib import request
from typing import Dict, List


class GridIntensity:
    WORLD_AVERAGE_INTENSITY = 475.0
    API_URL = "https://api.ember-energy.org/v1/carbon-intensity/yearly"
    ISO2_TO_ISO3 = {
        "BR": "BRA",
        "CA": "CAN",
        "CN": "CHN",
        "DE": "DEU",
        "ES": "ESP",
        "FR": "FRA",
        "GB": "GBR",
        "IN": "IND",
        "IT": "ITA",
        "JP": "JPN",
        "US": "USA",
    }

    def __init__(self, api_key=None):
        # Cache for grid intensity data
        self._intensity_data = None
        self.api_key = api_key if api_key is not None else os.getenv("EMBER_API_KEY")
        
    def _load_intensity_data(self) -> None:
        if self._intensity_data is None:
            self._intensity_data = {'WORLD': self.WORLD_AVERAGE_INTENSITY}
            if not self.api_key:
                return

            try:
                params = parse.urlencode({
                    "start_date": "2000",
                    "include_all_dates_value_range": "false",
                    "api_key": self.api_key,
                })
                with request.urlopen(f"{self.API_URL}?{params}", timeout=10) as response:
                    data = json.loads(response.read())
                    processed = self._process_ember_data(data)
                    if processed:
                        processed['WORLD'] = self.WORLD_AVERAGE_INTENSITY
                        self._intensity_data = processed
            except Exception:
                pass
    
    def _process_ember_data(self, data: Dict) -> Dict[str, float]:
        """Process Ember data into country-specific grid intensities."""
        processed = {}
        latest_by_country = {}
        entries = self._extract_entries(data)

        for entry in entries:
            country_code = self._country_code_from_entry(entry)
            intensity = entry.get('emissions_intensity_gco2_per_kwh')

            if not country_code or intensity is None:
                continue

            current = latest_by_country.get(country_code)
            if current is None or str(entry.get('date', '')) > str(current.get('date', '')):
                latest_by_country[country_code] = entry

        for country_code, entry in latest_by_country.items():
            processed[country_code] = float(entry['emissions_intensity_gco2_per_kwh'])

        return processed

    def _extract_entries(self, data: Dict) -> List[Dict]:
        entries = data.get('data', data) if isinstance(data, dict) else data
        if not isinstance(entries, list):
            return []
        return [entry for entry in entries if isinstance(entry, dict)]

    def _country_code_from_entry(self, entry: Dict) -> str:
        country_code = entry.get('entity_code') or entry.get('country_code')
        if not country_code:
            return ''
        return self._normalize_country_code(country_code)

    def _normalize_country_code(self, country_code: str) -> str:
        normalized = country_code.upper()
        return self.ISO2_TO_ISO3.get(normalized, normalized)
    
    def get_intensity(self, country_code: str = 'WORLD') -> float:
        self._load_intensity_data()
        normalized_country_code = self._normalize_country_code(country_code)
        return self._intensity_data.get(
            normalized_country_code,
            self._intensity_data['WORLD'],
        )
