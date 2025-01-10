from carbon_calculator import DataTransferEmissions, GreenDomains
import json


# Initialize calculators
emissions_calc = DataTransferEmissions()
green_domains = GreenDomains()

# Calculate emissions for 1GB of data transfer
result = emissions_calc.calculate_emissions(
    bytes_transferred=1024 * 1024 * 1024,  
    country_code='US'
)
print("Carbon Emissions Calculation:")
print(json.dumps(result, indent=2))

# Check if a domain is green
domain_result = green_domains.check_domain('google.com')
print("\nGreen Domain Check:")
print(json.dumps(domain_result, indent=2))