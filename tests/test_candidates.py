import unittest
from revenue_intake.candidates import normalize_candidate, normalize_feed

SOURCE = {
    "source_listing_id": "DEMO-001",
    "source_url": "https://example.org/listing/demo-001",
    "status": "available",
    "asking_price": "125,000",
    "arv_estimate": 210000,
}
OBSERVED = "2026-10-14T12:00:00Z"

class CandidateTests(unittest.TestCase):
    def test_default_is_fail_closed(self):
        data = normalize_candidate(SOURCE, OBSERVED)
        self.assertFalse(data["distribution_authorized"])
        self.assertFalse(data["publishable"])
        self.assertFalse(data["automated_marketing_eligible"])
        self.assertEqual(data["review_state"], "HUMAN_REVIEW_REQUIRED")

    def test_amounts_are_unverified_and_profit_not_inferred(self):
        data = normalize_candidate(SOURCE, OBSERVED)
        self.assertEqual(data["asking_price_usd_unverified"], "125000.00")
        self.assertEqual(data["arv_estimate_usd_unverified"], "210000.00")
        self.assertIsNone(data["realized_profit_usd"])

    def test_pending_or_sold_not_marketable(self):
        for status in ("pending", "sold", "unknown"):
            with self.subTest(status=status):
                data = normalize_candidate({**SOURCE, "status": status}, OBSERVED)
                self.assertIn("NOT_CONFIRMED_AVAILABLE", data["review_flags"])
                self.assertFalse(data["publishable"])

    def test_invalid_price_flagged(self):
        data = normalize_candidate({**SOURCE, "asking_price": "--"}, OBSERVED)
        self.assertIsNone(data["asking_price_usd_unverified"])
        self.assertIn("NO_VALID_ASKING_PRICE", data["review_flags"])

    def test_https_required(self):
        with self.assertRaises(ValueError):
            normalize_candidate({**SOURCE, "source_url": "http://example.org/listing"}, OBSERVED)

    def test_missing_identifier_fails(self):
        with self.assertRaises(ValueError):
            normalize_candidate({**SOURCE, "source_listing_id": ""}, OBSERVED)

    def test_timezone_required(self):
        with self.assertRaises(ValueError):
            normalize_candidate(SOURCE, "2026-10-14T12:00:00")

    def test_dedupes_only_same_source_listing(self):
        data = normalize_feed([SOURCE, SOURCE], OBSERVED)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["candidate_key"], "example.org:DEMO-001")

if __name__ == "__main__":
    unittest.main()
