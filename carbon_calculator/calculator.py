"""
Estimate carbon emissions from internet data transfer.

The model is the Sustainable Web Design Model (SWDM) version 4:
https://sustainablewebdesign.org/estimating-digital-emissions/

See docs/METHODOLOGY.md for the formulas, constants and limitations.
"""
from typing import Optional

from carbon_calculator.grid_intensity import GridIntensity

BYTES_PER_GB = 1_000_000_000  # SWDM uses decimal gigabytes (10^9 bytes).


class DataTransferEmissions:
    """SWDM v4 energy intensities in kWh per GB, split by system segment.

    Source: https://sustainablewebdesign.org/estimating-digital-emissions/
    (values derived from 5.29 ZB of global data transfer).
    """

    OPERATIONAL_KWH_PER_GB = {
        "data_centers": 0.055,
        "networks": 0.059,
        "user_devices": 0.080,
    }
    EMBODIED_KWH_PER_GB = {
        "data_centers": 0.012,
        "networks": 0.013,
        "user_devices": 0.081,
    }

    def __init__(self, grid_intensity: Optional[GridIntensity] = None):
        self.grid_intensity = grid_intensity or GridIntensity()

    def _intensity(self, country_code: str):
        """Return (gCO2e/kWh, source). Works with any object that has get_intensity."""
        info = getattr(self.grid_intensity, "get_intensity_info", None)
        if info is not None:
            return info(country_code)
        return self.grid_intensity.get_intensity(country_code), "custom"

    def calculate_emissions(
        self,
        bytes_transferred: int,
        country_code: str = "WORLD",
        green_hosting_factor: float = 0.0,
        include_embodied: bool = True,
        new_visitor_ratio: float = 1.0,
        return_visitor_ratio: float = 0.0,
        data_cache_ratio: float = 0.0,
    ):
        """Estimate emissions (gCO2e) for a data transfer.

        green_hosting_factor: share (0-1) of data center energy that is
            renewable. 1 if the host is verified green.
        include_embodied: also count manufacturing (embodied) emissions.
        new_visitor_ratio, return_visitor_ratio, data_cache_ratio: SWDM page
            view parameters (0-1). Defaults treat every transfer as uncached.
        """
        if bytes_transferred < 0:
            raise ValueError("bytes_transferred must be non-negative")
        for name, value in (
            ("green_hosting_factor", green_hosting_factor),
            ("new_visitor_ratio", new_visitor_ratio),
            ("return_visitor_ratio", return_visitor_ratio),
            ("data_cache_ratio", data_cache_ratio),
        ):
            if not 0 <= value <= 1:
                raise ValueError(f"{name} must be between 0 and 1")

        gb = bytes_transferred / BYTES_PER_GB
        intensity, source = self._intensity(country_code)

        segments = {}
        energy_kwh = 0.0
        for segment, op_kwh in self.OPERATIONAL_KWH_PER_GB.items():
            kwh = gb * op_kwh
            if include_embodied:
                kwh += gb * self.EMBODIED_KWH_PER_GB[segment]
            if segment == "data_centers":
                kwh *= 1 - green_hosting_factor
            segments[segment] = kwh
            energy_kwh += kwh

        # Cached data for returning visitors is not transferred again.
        visit_factor = new_visitor_ratio + return_visitor_ratio * (1 - data_cache_ratio)
        energy_kwh *= visit_factor
        emissions = {s: kwh * visit_factor * intensity for s, kwh in segments.items()}

        return {
            "bytes_transferred": bytes_transferred,
            "energy_consumed_kwh": round(energy_kwh, 6),
            "emissions_gco2e": round(energy_kwh * intensity, 6),
            "emissions_by_segment_gco2e": {s: round(v, 6) for s, v in emissions.items()},
            "country": country_code,
            "grid_intensity_gco2e_per_kwh": intensity,
            "grid_intensity_source": source,
            "model": "Sustainable Web Design Model v4",
            "includes_embodied": include_embodied,
        }
