"""
Query Green Web Foundation's Green Domains dataset.
"""
import json
from urllib import request, parse
from typing import Dict, Optional

class GreenDomains:
    API_URL = "https://api.thegreenwebfoundation.org/api/v3/greencheck/"
    
    def check_domain(self, domain: str) -> Dict:
        try:
            url = f"{self.API_URL}{parse.quote(domain)}"
            with request.urlopen(url) as response:
                data = json.loads(response.read())
                return {
                    'domain': domain,
                    'is_green': data.get('green', False),
                    'hosted_by': data.get('hostedby', 'Unknown'),
                    'hosted_by_website': data.get('hostedbywebsite', None)
                }
        except Exception as e:
            return {
                'domain': domain,
                'is_green': None,
                'error': str(e)
            }
