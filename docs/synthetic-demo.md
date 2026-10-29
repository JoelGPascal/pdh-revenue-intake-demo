# Runnable synthetic listing-intake demonstration

**Synthetic data only.** This example does not fetch listings, contact anyone, or write to a CRM.

From repository root, with Python 3.10+:

```bash
PYTHONPATH=src python - <<'PY'
from revenue_intake.candidates import normalize_feed

records = [
    {"source_listing_id": "demo-001", "source_url": "https://example.org/listing/demo-001",
     "status": "available", "asking_price": "$125,000", "arv_estimate": "190000",
     "property_address": "Synthetic Example Street"},
    {"source_listing_id": "demo-001", "source_url": "https://example.org/listing/demo-001",
     "status": "available", "asking_price": "$125,000", "arv_estimate": "190000",
     "property_address": "Synthetic Example Street"}
]
candidates = normalize_feed(records, "2026-10-29T10:00:00+00:00")
assert len(candidates) == 1
c = candidates[0]
assert c["candidate_key"] == "example.org:demo-001"
assert c["asking_price_usd_unverified"] == "125000.00"
assert c["arv_estimate_usd_unverified"] == "190000.00"
assert c["realized_profit_usd"] is None
assert c["review_state"] == "HUMAN_REVIEW_REQUIRED"
assert c["distribution_authorized"] is False
assert c["publishable"] is False
assert c["automated_marketing_eligible"] is False
print(c["candidate_key"], c["review_state"], c["publishable"])
PY
```

Expected printed line (illustrative; not captured from execution):

```text
example.org:demo-001 HUMAN_REVIEW_REQUIRED False
```

## Test suite

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

The eight source-defined cases cover fail-closed defaults, unverified financial fields, sold/pending status, invalid prices, HTTPS requirement, missing IDs, timezone requirement and source-key deduplication. The repository reports eight passing local tests on 2026-10-14; this documentation update did not rerun them.

**Not implemented:** rights-to-market verification, source authenticity checks, CRM mutations, outreach consent, live feed, scraping, automated publication or revenue calculations.
