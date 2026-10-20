import json

from carbon_calculator import DataTransferEmissions, GreenDomains

emissions_calc = DataTransferEmissions()
green_domains = GreenDomains()

# Emissions for 1 GB (10^9 bytes) of data transfer, world-average grid.
result = emissions_calc.calculate_emissions(bytes_transferred=1_000_000_000)
print("Carbon emissions estimate:")
print(json.dumps(result, indent=2))

# Check whether a domain is hosted green.
domain_result = green_domains.check_domain("google.com")
print("\nGreen domain check:")
print(json.dumps(domain_result, indent=2))
