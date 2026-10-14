# Intake Control Architecture — Public Case Study

**Status:** proof of concept, locally tested on 2026-10-14. No external live deployment.

| Boundary | Input | Output | Safeguard |
|---|---|---|---|
| External source | Untrusted listing ID, URL, advertised price, optional estimated ARV and status | Candidate record | No claims of authority or realized returns |
| Normalizer | Listing record + timezone-aware observation time | Source identity, UTC timestamp, labelled unverified fields | Reject bad IDs, non-HTTPS URLs, naive timestamps |
| Review rules | Source status, optional address, advertised figures | Explicit review flags | Never inferred marketing authority |
| Downstream gate | Candidate record | Human-review-required record | Never produces publication-ready or outbound-ready status |

**Deliberately absent:** live CRM API, actor web scraping logic, contracts, buyer contact information, personal data, dialling, bulk SMS, auto-publishing, company financial projections and credential material.

**Measured evidence:** 8 synthetic-data local unit tests passed on 2026-10-14. No production reliability, revenue impact or closed-loop operational outcome is claimed.

**Security note:** The module is an illustrative control, not a general-purpose URL sanitiser or a production authorization service. Additional provenance verification, permission audits, retries, storage and tamper-resistant logs would be required before a live deployment.
