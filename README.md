# PDH Revenue Intake Demo

A Python prototype that turns third-party property listing inputs into structured records for human review.

## Project summary

**Problem:** Inconsistent listing data makes it difficult to distinguish a sourced lead from a verified commercial opportunity.

**My contribution:** I defined normalization, source tracking and review requirements from PDH operating needs and developed the prototype with AI coding assistance.

**Demonstrated result:** Synthetic records are normalized, duplicate source IDs are collapsed and uncertain fields receive review flags. Eight offline tests were reproduced on October 29, 2026.

**Start here:** [Runnable example](docs/synthetic-demo.md) · [Architecture](docs/architecture.md) · [Commercial context](docs/COMMERCIAL_CONTEXT.md)

This is a synthetic-data demonstration. Live CRM integration and outreach are outside its implemented scope.

## Problem
An external property marketplace may provide price, ARV estimates, availability labels and IDs, but none of those alone prove:
- the property is actually available, under contract, or assignable;
- the operator has permission to remarket it;
- a consumer opted in to email, SMS or AI calls;
- an estimate of ARV minus asking price is profit.

Blindly passing scraped fields to a CRM, public website or outbound tool can cause false claims and unauthorised marketing.

## What is implemented
- Pure Python normalization of a third-party source record, with a stable source identity key.
- UTC observation timestamps, explicit *unverified* price/ARV fields, source-status labelling.
- **Fail-closed controls:** `distribution_authorized=False`, `publishable=False`, `automated_marketing_eligible=False`, `HUMAN_REVIEW_REQUIRED`.
- Sold/pending/unknown statuses, missing price/address and unverified ARV receive review flags.
- Duplicate source-listing keys collapse without ever merging or editing CRM buyer contacts.
- Synthetic-data unit tests, with no external network access or real customer data.

## Run tests
Python 3.10+; no third-party dependencies.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

**Local check, 2026-10-14: 8 tests passed, 0 failures. Independent offline reproduction, 2026-10-29: 8 tests passed, 0 failures.** This test result covers the demonstration's pure functions, not production deployments or integrated APIs. GitHub CI and independent Codex review are not yet complete.

## Architecture
```
Third-party listing sample
    ↓ normalize and tag unverified fields
    ↓ source-ID-only deduplication
Human review queue (not a deal)
    ↓ verify facts, rights, contact permissions, underwriting
    ↓ separate explicit human approval and production safeguards
Potential CRM intake (NOT implemented here)
```

**This repository cannot send, publish, or update anything.** The operational PDH CRM, buyer database, contracts, credentials, API tokens and live integration code are deliberately excluded.

## Next engineering work (not completed)
1. Native GoHighLevel object/field/workflow inventory and duplicate-safe buyer reconciliation.
2. Contract/right-to-market authorization evidence as an independent decision gate.
3. Independent tests for Property → Contact/Opportunity associations; no processed state without verified links.
4. Controlled, compliant buyer-matching and outreach only after permission and business-case validation.

## Related proof
- [Public CRM Association Verifier](https://github.com/JoelGPascal/crm-association-verifier) — distinct read-only record-relation verification project.
- [Current recruiter-facing portfolio — Enterprise Sales, GTM & Practical AI](https://app.notion.com/p/40b5622002f981709ab3e773187085f3)

**Visibility:** this source repository is public; no license for redistribution is granted in this release.

## Engineering review package (2026-10-29)

- [Architecture, provenance and trust boundaries](docs/architecture.md)
- [Runnable synthetic input/output demonstration](docs/synthetic-demo.md)

The demonstration is provided for independent local execution; this update did not run the suite or deploy an integration.

- [Security and operational readiness checkpoint (2026-10-29)](docs/READINESS_2026-10-29.md)
