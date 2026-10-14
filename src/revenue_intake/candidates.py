"""Review-only normalisation of third-party property listings.

Source data does not provide contract rights, contact consent, or realised profit.
This module has no networking or external side effects.
"""
from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable
from urllib.parse import urlparse


def _positive_usd(value: Any) -> str | None:
    if value is None or str(value).strip() == "":
        return None
    try:
        num = Decimal(str(value).strip().replace(",", "").replace("$", ""))
    except (InvalidOperation, ValueError):
        return None
    if not num.is_finite() or num <= 0:
        return None
    return str(num.quantize(Decimal("0.01")))


def normalize_candidate(record: dict[str, Any], observed_at: str) -> dict[str, Any]:
    """Create a research candidate, never an automatically marketable deal."""
    observed = datetime.fromisoformat(observed_at.replace("Z", "+00:00"))
    if observed.tzinfo is None:
        raise ValueError("observed_at requires a timezone")
    source_id = str(record.get("source_listing_id") or "").strip()
    if not source_id or len(source_id) > 150:
        raise ValueError("valid source listing ID required")
    source_url = str(record.get("source_url") or "").strip()
    parsed = urlparse(source_url)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError("source_url must be a valid HTTPS web address")
    status = str(record.get("status") or "unknown").strip().lower()
    if status not in {"available", "pending", "sold", "unknown"}:
        status = "unknown"
    asking = _positive_usd(record.get("asking_price"))
    arv = _positive_usd(record.get("arv_estimate"))
    flags = ["MARKETING_RIGHTS_NOT_VERIFIED"]
    if status != "available":
        flags.append("NOT_CONFIRMED_AVAILABLE")
    if not asking:
        flags.append("NO_VALID_ASKING_PRICE")
    if not record.get("property_address"):
        flags.append("EXACT_ADDRESS_NOT_PROVIDED")
    if arv is not None:
        flags.append("SOURCE_ARV_NOT_INDEPENDENTLY_VERIFIED")
    return {
        "candidate_key": f"{parsed.hostname.lower()}:{source_id}",
        "observed_at_utc": observed.astimezone(timezone.utc).isoformat(),
        "source_url": source_url,
        "source_status_unverified": status,
        "asking_price_usd_unverified": asking,
        "arv_estimate_usd_unverified": arv,
        "realized_profit_usd": None,
        "distribution_authorized": False,
        "publishable": False,
        "automated_marketing_eligible": False,
        "review_state": "HUMAN_REVIEW_REQUIRED",
        "review_flags": flags,
    }


def normalize_feed(records: Iterable[dict[str, Any]], observed_at: str) -> list[dict[str, Any]]:
    """Remove duplicate source candidates, not duplicate buyers or contacts."""
    unique = {}
    for record in records:
        candidate = normalize_candidate(record, observed_at)
        unique[candidate["candidate_key"]] = candidate
    return list(unique.values())
