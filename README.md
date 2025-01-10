# Carbon Calculator

A Python library for calculating carbon emissions from internet data transfer and checking green hosting status.

## Features

- Calculate carbon emissions from data transfer
- Get grid intensity data by country
- Check domains against Green Web Foundation's dataset

## Usage

```python
from carbon_calculator import DataTransferEmissions, GreenDomains

# Calculate emissions
calc = DataTransferEmissions()
result = calc.calculate_emissions(
    bytes_transferred=1024 * 1024 * 1024,  # 1GB
    country_code='US'
)

# Check if a domain is green
domains = GreenDomains()
green_status = domains.check_domain('example.com')
```

## Data Sources

- Grid intensity data: Ember Climate Data Portal
- Green domains: Green Web Foundation API
- Energy consumption model based on peer-reviewed research

## Notes

- All calculations are estimates based on available data
- Grid intensity data is updated periodically
- Free APIs are used for all external data