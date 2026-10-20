# CO2.py

[![tests](https://github.com/InesZenkri/CO2.py/actions/workflows/tests.yml/badge.svg)](https://github.com/InesZenkri/CO2.py/actions/workflows/tests.yml)

Python library that estimates the carbon emissions of internet data transfer using the
[Sustainable Web Design Model v4](https://sustainablewebdesign.org/estimating-digital-emissions/),
and checks whether a domain is hosted green via the Green Web Foundation.

## Features

- Emissions per segment (data centers, networks, user devices), operational and embodied
- Country grid intensity from the [Ember API](https://api.ember-energy.org/v1/docs), with a documented world-average fallback
- Green hosting check with the [Green Web Foundation Greencheck API](https://api.thegreenwebfoundation.org/api/v3/greencheck/google.com)
- No runtime dependencies (standard library only)

## Install

```bash
pip install .
```

## Usage

```python
from carbon_calculator import DataTransferEmissions

calculator = DataTransferEmissions()
result = calculator.calculate_emissions(
    bytes_transferred=1_000_000_000,   # 1 GB
    country_code="DE",
)
print(result)
```

Output for 1 GB without an Ember API key (world average of 494 gCO2e/kWh is used and
reported as such):

```python
{
    "bytes_transferred": 1000000000,
    "energy_consumed_kwh": 0.3,
    "emissions_gco2e": 148.2,
    "emissions_by_segment_gco2e": {
        "data_centers": 33.098,
        "networks": 35.568,
        "user_devices": 79.534,
    },
    "country": "DE",
    "grid_intensity_gco2e_per_kwh": 494.0,
    "grid_intensity_source": "world_average",
    "model": "Sustainable Web Design Model v4",
    "includes_embodied": True,
}
```

Options: `green_hosting_factor`, `include_embodied`, `new_visitor_ratio`,
`return_visitor_ratio`, `data_cache_ratio`. See [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

Check a domain:

```python
from carbon_calculator import GreenDomains

print(GreenDomains().check_domain("google.com"))
# {'domain': 'google.com', 'is_green': True, 'hosted_by': 'Google Cloud', 'hosted_by_website': 'https://cloud.google.com'}
```

Network errors are returned as `{"domain": ..., "is_green": None, "error": "..."}`.

## Country grid intensity

Get a free API key at https://ember-energy.org/data/api/ and set it:

```bash
export EMBER_API_KEY="your-api-key"
```

Without a key, or if a country is missing or the API fails (a warning is logged), the
world average is used and `grid_intensity_source` is `world_average`. Countries need an
ISO 3166-1 alpha-3 code (alpha-2 works for a short built-in list).

## Methodology and sources

Full formulas, constants, limitations and references: [docs/METHODOLOGY.md](docs/METHODOLOGY.md).

| Item | Source |
|------|--------|
| Energy model | Sustainable Web Design Model v4, https://sustainablewebdesign.org/estimating-digital-emissions/ |
| Grid intensity | Ember, https://ember-energy.org/data/ (CC BY 4.0) |
| Green hosting | Green Web Foundation, https://www.thegreenwebfoundation.org/ |
| Cross-check | CO2.js, https://developers.thegreenwebfoundation.org/co2js/models/overview/ |

These are estimates, not audited figures.

## Development

```bash
python3 -m unittest discover -s tests
```

## License

MIT, see [LICENSE](LICENSE).
