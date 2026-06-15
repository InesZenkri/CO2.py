# Carbon Calculator

CO2.py is a Python library for calculating carbon emissions from internet data transfer and checking green hosting status.

## Features

- Calculate carbon emissions from data transfer
- Get grid intensity data by country
- Check domains against Green Web Foundation's dataset


## Install the Library Locally:
Navigate to the root directory of your project (where setup.py is located) and run:
```bash
pip install .
```
This will install your package locally, allowing you to import it in other projects or scripts.

## Usage

Calculate estimated emissions for 1 GiB of transfer:

```python
from carbon_calculator import DataTransferEmissions

calculator = DataTransferEmissions()
result = calculator.calculate_emissions(
    bytes_transferred=1024 * 1024 * 1024,
    country_code="US",
)

print(result)
```

Example output without an Ember API key:

```python
{
    "bytes_transferred": 1073741824,
    "energy_consumed_kwh": 0.06,
    "emissions_gco2": 28.5,
    "country": "US",
    "grid_intensity_gco2_per_kwh": 475.0,
}
```

Check a domain against the Green Web Foundation API:

```python
from carbon_calculator import GreenDomains

green_domains = GreenDomains()
print(green_domains.check_domain("google.com"))
```

Network errors are returned as an error object:

```python
{
    "domain": "google.com",
    "is_green": None,
    "error": "network unavailable",
}
```

## Grid Intensity Data

`GridIntensity` uses Ember's documented carbon intensity API:

```text
https://api.ember-energy.org/v1/carbon-intensity/yearly
```

Set `EMBER_API_KEY` to fetch country-specific grid intensity data:

```bash
export EMBER_API_KEY="your-api-key"
```

If no API key is configured, if the API is unavailable, or if a country is not found, the library falls back to `475.0 gCO2/kWh` as a world-average estimate.

## Data Sources

- Grid intensity data: Ember API, `/v1/carbon-intensity/yearly`
- Green domains: Green Web Foundation API
- Energy consumption model based on peer-reviewed research

## Development

Run the test suite:

```bash
python3 -m unittest discover -s tests
```

Run a syntax check:

```bash
python3 -m compileall carbon_calculator example.py setup.py tests
```

## Notes

- All calculations are estimates based on available data
- Country-specific grid intensity requires an Ember API key
- Green Web Foundation checks require network access
