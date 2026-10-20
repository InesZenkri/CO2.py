"""
Query the Green Web Foundation's Greencheck API.

API: https://api.thegreenwebfoundation.org/api/v3/greencheck/<domain>
"""
import json
from typing import Dict
from urllib import parse, request


class GreenDomains:
    API_URL = "https://api.thegreenwebfoundation.org/api/v3/greencheck/"

    def check_domain(self, domain: str) -> Dict:
        if not domain:
            raise ValueError("domain is required")

        try:
            url = f"{self.API_URL}{parse.quote(domain)}"
            with request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read())
            # The API returns hosted_by / hosted_by_website. The old
            # hostedby / hostedbywebsite keys are still read as a fallback.
            return {
                "domain": domain,
                "is_green": bool(data.get("green", False)),
                "hosted_by": data.get("hosted_by") or data.get("hostedby") or "Unknown",
                "hosted_by_website": data.get("hosted_by_website") or data.get("hostedbywebsite"),
            }
        except Exception as e:
            return {"domain": domain, "is_green": None, "error": str(e)}
