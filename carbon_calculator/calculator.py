"""
Calculate carbon emissions from data transfer.
"""
from typing import Optional

from carbon_calculator.grid_intensity import GridIntensity


class DataTransferEmissions:
    # Based on: https://www.academia.edu/15190649/The_Energy_Intensity_of_the_Internet_Edge_and_Core_Networks
    ENERGY_PER_GB = 0.06  

    def __init__(self, grid_intensity: Optional[GridIntensity] = None):
        self.grid_intensity = grid_intensity or GridIntensity()

    def calculate_emissions(
        self,
        bytes_transferred: int,
        country_code: str = 'WORLD'
    ):
        if bytes_transferred < 0:
            raise ValueError("bytes_transferred must be non-negative")

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
