# Research Log – CardAdvisor

## Django

Topics reviewed:

- Django project and app structure
- Template inheritance (`base.html`, `{% block %}`)
- URL routing with app-level `urls.py`
- Separation of concerns (views vs business logic)
- Service layer pattern for non-model logic

Reference: Django documentation (templates, project structure)

---

## django-tailwind

Topics reviewed:

- Installing django-tailwind
- Theme app creation
- Tailwind watcher (`tailwind dev`)
- Using `{% tailwind_css %}` in base template
- Keeping compiled CSS inside theme app

---

## UI Inspiration Research

Studied the old Ramp.com landing page for:

- Dark gradient hero layout
- Left-aligned headline + right mock dashboard
- Input-style CTA block
- Mobile-first collapse of two-column layout

Adapted for:

- Fintech decision tool instead of marketing site
- Minimal sections
- Data-driven tone

---

## Credit Card Domain Research

Reviewed common credit card comparison criteria:

Source: PaisaBazaar (general reward structures)

Key factors identified:

- Cashback rates by category
- Reward caps per month
- Annual fees and waiver thresholds
- Lounge access as fixed-value benefit
- Forex markup as cost factor
- Category-specific multipliers (online, fuel, dining, travel)

These factors will be modeled as structured data rather than hardcoded logic.

---

## AI Usage

AI was used for:

- Setting up the base template for the project
- Structuring the project architecture
- Debugging issues with the landing pages 
- Drafting documentation templates

AI is **not** used for scoring or ranking logic.
The decision engine will be deterministic and explainable.

## Credit Card Data Sources

Primary reference for card features and reward structures:

- PaisaBazaar (card fees, category cashback, lounge availability)
- Individual card product pages (issuer sites) for fee and lounge confirmation

Used these to identify:

- Category-based reward patterns (online, fuel, dining, travel)
- Fee waiver thresholds
- Forex markup ranges
- Lounge access presence/absence

## Handling Ambiguity

Exact reward caps and income requirements vary by variant and are not consistently published.

Resolution approach:
- Used representative values aligned with typical ranges
- Prioritized structural accuracy (which category earns more) over exact numbers

This is documented as an assumption in README.

## Community References

Reddit threads (r/IndiaInvestments, r/CreditCardsIndia) were used to:
- Validate typical effective cashback rates
- Understand real user-reported caps and redemption behavior
- Confirm that UPI-based cards (e.g., Kiwi) behave closer to flat cashback in practice

These were used only to cross-check ranges, not as authoritative sources.

## AI Usage Today

AI was used for:
- Structuring the Django data model
- Designing the reward seeding command, to avoid manual entry and save time.

AI was not used to generate reward values or ranking logic.