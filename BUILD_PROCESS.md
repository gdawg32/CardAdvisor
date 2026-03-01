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

## Phase 5 – Data Layer Implementation

Defined normalized data models:

- CreditCard
- RewardCategory (one-to-many)

Rationale:
Reward rules vary by category and card, so storing them in a separate table avoids hardcoding and supports dynamic evaluation.

Created database migrations and registered both models in Django admin.  
Entered 11 cards covering different reward strategies (online cashback, flat cashback, fuel-focused, dining/travel, lounge-heavy, UPI-first).

To avoid repetitive manual entry of reward rules, implemented a custom Django management command (`seed_rewards`) to populate RewardCategory records programmatically with the help of ChatGPT.

Encountered an issue where the command was not detected due to incorrect folder naming (`managements` instead of `management`).  
Resolved by fixing directory name.

Current status:
- Data model complete
- Dataset populated
- Reward rules seeded and verified in admin

Next step:
Implement deterministic decision engine as a service module and validate outputs in Django shell before UI integration.

## Form Design and Input Modeling

The input interface was redesigned from a simple numeric form into a structured decision profile.

Instead of only collecting spend values, the form now captures:

- Category-wise monthly spend (online, fuel, dining, travel, groceries, other)
- Foreign spend
- Annual income
- Fee tolerance
- Preference toggles (cashback, lounge, low fee, low forex)

The preference toggles are converted into a normalized weight vector used by the decision engine.  
A special case was introduced where selecting only “low forex” acts as a hard constraint and filters out cards that do not support international transactions.

This separates feasibility constraints from scoring logic.


## Decision Engine Evolution

### V1 – Net Value Only

The initial implementation ranked cards purely on:

net value = rewards + lounge value − annual fee − forex cost

While financially correct, it ignored user preferences and produced identical rankings for different user goals.


### V2 – Constraint + Multi-Criteria Model

The engine was refactored into three stages:

1. **Hard constraints**
   - Income eligibility
   - Fee tolerance
   - Forex support (when user prioritises low forex)

2. **Monetary evaluation**
   - Category-wise reward calculation with spend and cashback caps
   - Fee waiver logic based on annual spend
   - Lounge visits converted into a monetary value
   - Forex cost applied only when supported

3. **Normalized multi-criteria scoring**
   - Cashback, lounge value, fee, and forex cost are min–max normalized
   - Cost metrics are inverted
   - A weighted composite score is computed from user preferences
   - Final score combines normalized net value and composite score

Stable tie-breaking was added using:
composite score → lower fee → higher cashback → card name


## Refactoring Decisions

- Replaced overly abstract helper layers with a more linear and readable flow
- Reduced defensive programming where unnecessary
- Consolidated reward logic into a single monthly calculation path
- Moved eligibility checks before reward computation for efficiency
- Added explicit forex support handling to avoid penalizing RuPay UPI cards
- Treated zero-fee cards as automatically “fee waived” for clarity in UI output


## Explainability Additions

Each card now returns:

- Category-wise annual reward breakdown
- Top contributing category
- Effective fee and waiver status
- Forex cost
- Net annual value

This allows the UI to explain *why* a card was recommended.


## AI Usage in Development

AI tools (ChatGPT) were used in a limited and transparent manner for:

- Exploring alternative decision engine structures
- Introducing normalization and composite scoring utilities
- Reviewing edge cases such as cashback caps and forex eligibility
- Refactoring code for readability and removal of unused abstractions

All architectural decisions, domain modeling, and business logic validation were implemented manually.

AI was also used to format Markdown documentation into a consistent and readable structure.