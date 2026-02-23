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