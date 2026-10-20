import unittest
from unittest.mock import patch

from carbon_calculator import DataTransferEmissions, GreenDomains, GridIntensity


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def read(self):
        return self.payload.encode("utf-8")


class FakeGridIntensity:
    def get_intensity(self, country_code):
        return 400.0


class DataTransferEmissionsTests(unittest.TestCase):
    def test_swdm_v4_one_gb(self):
        # 1 GB, 400 g/kWh. Operational 0.194 + embodied 0.106 = 0.300 kWh/GB.
        calculator = DataTransferEmissions(grid_intensity=FakeGridIntensity())

        result = calculator.calculate_emissions(
            bytes_transferred=1_000_000_000,
            country_code="DE",
        )

        self.assertAlmostEqual(result["energy_consumed_kwh"], 0.300, places=6)
        self.assertAlmostEqual(result["emissions_gco2e"], 120.0, places=4)
        self.assertEqual(result["grid_intensity_gco2e_per_kwh"], 400.0)
        self.assertEqual(result["grid_intensity_source"], "custom")

    def test_operational_only(self):
        calculator = DataTransferEmissions(grid_intensity=FakeGridIntensity())

        result = calculator.calculate_emissions(
            bytes_transferred=1_000_000_000, include_embodied=False
        )

        self.assertAlmostEqual(result["energy_consumed_kwh"], 0.194, places=6)

    def test_green_hosting_removes_data_center_energy(self):
        calculator = DataTransferEmissions(grid_intensity=FakeGridIntensity())

        result = calculator.calculate_emissions(
            bytes_transferred=1_000_000_000, green_hosting_factor=1.0
        )

        self.assertEqual(result["emissions_by_segment_gco2e"]["data_centers"], 0.0)
        self.assertAlmostEqual(result["energy_consumed_kwh"], 0.300 - 0.067, places=6)

    def test_cached_return_visits(self):
        calculator = DataTransferEmissions(grid_intensity=FakeGridIntensity())

        full = calculator.calculate_emissions(bytes_transferred=1_000_000_000)
        cached = calculator.calculate_emissions(
            bytes_transferred=1_000_000_000,
            new_visitor_ratio=0.25,
            return_visitor_ratio=0.75,
            data_cache_ratio=0.02,
        )

        expected = 0.25 + 0.75 * 0.98
        self.assertAlmostEqual(
            cached["energy_consumed_kwh"], full["energy_consumed_kwh"] * expected, places=5
        )

    def test_rejects_invalid_ratio(self):
        calculator = DataTransferEmissions(grid_intensity=FakeGridIntensity())

        with self.assertRaises(ValueError):
            calculator.calculate_emissions(bytes_transferred=1, green_hosting_factor=1.5)

    def test_rejects_negative_bytes(self):
        calculator = DataTransferEmissions(grid_intensity=FakeGridIntensity())

        with self.assertRaises(ValueError):
            calculator.calculate_emissions(bytes_transferred=-1)


class GridIntensityTests(unittest.TestCase):
    def test_uses_world_average_without_api_key(self):
        grid_intensity = GridIntensity(api_key="")

        self.assertEqual(grid_intensity.get_intensity("US"), 494.0)

    def test_falls_back_to_world_average_for_unknown_country(self):
        grid_intensity = GridIntensity()
        grid_intensity._intensity_data = {"WORLD": 494.0}

        self.assertEqual(grid_intensity.get_intensity("XX"), 494.0)

    def test_processes_current_ember_api_response_shape(self):
        grid_intensity = GridIntensity()

        result = grid_intensity._process_ember_data({
            "data": [
                {
                    "entity_code": "DEU",
                    "date": "2023",
                    "emissions_intensity_gco2_per_kwh": 360.0,
                },
                {
                    "entity_code": "DEU",
                    "date": "2024",
                    "emissions_intensity_gco2_per_kwh": 350.5,
                },
                {
                    "entity_code": None,
                    "date": "2024",
                    "emissions_intensity_gco2_per_kwh": 100,
                },
            ],
        })

        self.assertEqual(result, {"DEU": 350.5})

    @patch("carbon_calculator.grid_intensity.request.urlopen")
    def test_fetches_intensity_with_api_key(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(
            '{"data": [{"entity_code": "USA", "date": "2024", '
            '"emissions_intensity_gco2_per_kwh": 370.0}]}'
        )

        grid_intensity = GridIntensity(api_key="test-key")

        self.assertEqual(grid_intensity.get_intensity("US"), 370.0)
        self.assertIn("api_key=test-key", mock_urlopen.call_args[0][0])

    @patch("carbon_calculator.grid_intensity.request.urlopen")
    def test_falls_back_when_api_request_fails(self, mock_urlopen):
        mock_urlopen.side_effect = OSError("network unavailable")

        grid_intensity = GridIntensity(api_key="test-key")

        self.assertEqual(grid_intensity.get_intensity("USA"), 494.0)


class GreenDomainsTests(unittest.TestCase):
    @patch("carbon_calculator.green_domains.request.urlopen")
    def test_reads_legacy_key_names(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(
            '{"green": false, "hostedby": "Old Host", "hostedbywebsite": null}'
        )

        result = GreenDomains().check_domain("example.org")

        self.assertFalse(result["is_green"])
        self.assertEqual(result["hosted_by"], "Old Host")

    def test_rejects_empty_domain(self):
        with self.assertRaises(ValueError):
            GreenDomains().check_domain("")

    @patch("carbon_calculator.green_domains.request.urlopen")
    def test_checks_domain_with_mocked_api_response(self, mock_urlopen):
        mock_urlopen.return_value = FakeResponse(
            '{"green": true, "hosted_by": "Example Host", '
            '"hosted_by_website": "https://example.com"}'
        )

        result = GreenDomains().check_domain("example.com")

        self.assertEqual(result, {
            "domain": "example.com",
            "is_green": True,
            "hosted_by": "Example Host",
            "hosted_by_website": "https://example.com",
        })


if __name__ == "__main__":
    unittest.main()
