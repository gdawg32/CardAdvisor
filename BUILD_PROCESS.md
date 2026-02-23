# Build Process – CardAdvisor

## Phase 1 – Problem Framing

The assignment requires a decision companion system with:

- Multiple options
- Criteria with weights
- Explainable ranking

I selected credit card selection because it has:

- Quantifiable benefits (cashback, lounge, fees)
- Real constraints (caps, eligibility)
- Clear scoring logic
- Retail relevance

The goal is to compute net annual value based on user spending.

---

## Phase 2 – Project Setup

Steps:

1. Created Django project and core app
2. Integrated Tailwind CSS using django-tailwind
3. Used Claude AI in helping set up the base template of the website
4. Verified Tailwind watcher using `python manage.py tailwind dev`

---

## Phase 3 – Frontend Foundation

Implemented:

- Base template with Tailwind
- Mobile-responsive navbar with collapsible menu
- Hero section inspired by Ramp layout
- CTA input block (placeholder for decision form)
- “How it works” section

Design goals:

- Mobile-first
- Minimal text
- Clear primary action
- Reusable layout

No business logic is placed in templates.

---

## Phase 4 – Architecture Planning

Planned separation:

- Models → credit card data
- Services → decision engine
- Views → request handling only
- Templates → presentation

This avoids mixing scoring logic with UI.

---

## Current Status

Completed:

- UI shell
- Template system
- Tailwind integration
- Navigation and hero layout

Pending:

- Data model design
- Admin data entry
- Decision engine
- Result rendering

---

## Next Steps

1. Implement CreditCard and RewardCategory models
2. Load sample dataset via Django admin
3. Build decision engine as a service function
4. Connect form → engine → ranked output