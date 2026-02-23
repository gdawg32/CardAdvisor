# CardAdvisor – Credit Card Decision Companion

## Problem Understanding

Retail users often select credit cards based on marketing or incomplete comparisons.  
The actual value of a card depends on individual spending patterns, reward caps, annual fees, and category multipliers.

CardAdvisor is a decision companion system that:

- Accepts user spending patterns
- Evaluates multiple credit cards
- Computes net annual value
- Produces a ranked, explainable recommendation

The system is deterministic and explainable, not a black-box AI model.

---

## Current Scope (MVP – Phase 1)

Completed:

- Django project setup
- Tailwind CSS integration using `django-tailwind`
- Mobile-first responsive landing page
- Ramp-inspired hero layout with CTA
- Base template with reusable navbar
- Template inheritance structure

Not yet implemented:

- Credit card data models
- Decision engine
- Result ranking logic

---

## System Direction

Planned architecture:

User Input → Django View → Decision Engine (service layer) →  
CreditCard + RewardCategory models → Ranked Output → Template

The decision engine will compute:

- Annual reward value per category
- Lounge value (assumed constant per visit)
- Fee waiver logic
- Net annual benefit
- Weighted score

---

## Design Principles

- Explainable scoring (no hidden AI decisions)
- Normalized data model for reward categories
- Service-layer business logic (not inside views)
- Mobile-first UI
- Deterministic outputs for the same input

---

## Assumptions (Planned)

- Reward points will be converted to ₹ using a fixed rate
- Lounge visit value will be assumed as a constant ₹ amount
- Monthly reward caps will be applied before annualization
- Fee waiver will be applied if annual spend crosses threshold

---

## How to Run

```bash
python -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt

python manage.py tailwind dev

Open: http://127.0.0.1:8000/
```
---

