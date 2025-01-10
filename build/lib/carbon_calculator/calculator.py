"""
Calculate carbon emissions from data transfer.
"""
import json
from urllib import request
from typing import Optional, Dict, Union
from carbon_calculator.grid_intensity import GridIntensity
class DataTransferEmissions:
    # Based on: https://www.nature.com/articles/s41598-020-76125-y
    ENERGY_PER_GB = 0.06  # kWh/GB

    def __init__(self):
        self.grid_intensity = GridIntensity()

    def calculate_emissions(
        self,
        bytes_transferred: int,
        country_code: str = 'WORLD'
    ) -> Dict[str, Union[float, str]]:
        """
        Calculate CO2 emissions from data transfer.
        
        Args:
            bytes_transferred: Number of bytes transferred
            country_code: ISO 3166-1 alpha-2 country code
            
        Returns:
            Dictionary containing emissions data
        """
        gb_transferred = bytes_transferred / (1024 ** 3)  
        energy_consumed = gb_transferred * self.ENERGY_PER_GB
        
        # Get grid intensity for the country (gCO2/kWh)
        grid_intensity = self.grid_intensity.get_intensity(country_code)
        
        # Calculate emissions (gCO2)
        emissions = energy_consumed * grid_intensity
        
        return {
            'bytes_transferred': bytes_transferred,
            'energy_consumed_kwh': round(energy_consumed, 6),
            'emissions_gco2': round(emissions, 6),
            'country': country_code,
            'grid_intensity_gco2_per_kwh': grid_intensity
        }