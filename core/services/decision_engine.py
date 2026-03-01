from typing import Any, Dict, Optional

from django.db.models import Prefetch

from core.models import CreditCard, RewardCategory

LOUNGE_VALUE_PER_VISIT = 800.0
DEFAULT_WEIGHTS = {"cashback": 0.6, "lounge": 0.2, "fee": 0.15, "forex": 0.05}
TIE_EPSILON = 1.0


# small utilities
def to_float(val: Any) -> float:
    try:
        f = float(val)
        return f if f >= 0 else 0.0
    except Exception:
        return 0.0


def normalize(value: float, low: float, high: float) -> float:
    if high == low:
        return 1.0
    return (value - low) / (high - low)


# reward calculation per rule
def monthly_reward(spend: float, rate: float, cap_type: str, cap: Optional[float]) -> float:
    if spend <= 0 or rate <= 0:
        return 0.0

    reward = spend * rate

    if cap is None or cap_type == "none":
        return reward

    cap = float(cap)

    if cap_type == "spend":
        return min(spend, cap) * rate

    if cap_type == "cashback":
        return min(reward, cap)

    return reward


# main engine
def evaluate_cards(
    user_input: Dict[str, Any],
    weights: Optional[Dict[str, float]] = None,
    alpha: float = 0.75,
    include_ineligible: bool = True,
) -> Dict[str, Any]:

    categories = ["online", "fuel", "dining", "travel", "groceries", "other"]

    monthly_spend = {c: to_float(user_input.get(c, 0)) for c in categories}
    monthly_foreign = to_float(user_input.get("monthly_foreign", 0))
    annual_income = to_float(user_input.get("annual_income", 0))
    fee_tolerance = user_input.get("fee_tolerance")
    fee_tolerance = to_float(fee_tolerance) if fee_tolerance is not None else None

    enforce_low_forex = bool(user_input.get("enforce_low_forex", False))

    if weights:
        total = sum(weights.values())
        if total > 0:
            weights = {k: v / total for k, v in weights.items()}
        else:
            weights = DEFAULT_WEIGHTS.copy()
    else:
        weights = DEFAULT_WEIGHTS.copy()

    annual_spend = sum(monthly_spend.values()) * 12

    cards = CreditCard.objects.prefetch_related(
        Prefetch("reward_categories", queryset=RewardCategory.objects.all())
    )

    eligible = []
    ineligible = []

    for card in cards:
        meta = {"card_id": card.id, "name": card.name, "issuer": card.issuer}

        # eligibility checks 
        if annual_income < card.min_income_required:
            ineligible.append({**meta, "eligible": False, "reason_ineligible": "Income below eligibility"})
            continue

        if fee_tolerance is not None and card.annual_fee > fee_tolerance:
            ineligible.append({**meta, "eligible": False, "reason_ineligible": "Annual fee exceeds tolerance"})
            continue

        if enforce_low_forex and not card.supports_forex:
            ineligible.append(
                {
                    **meta,
                    "eligible": False,
                    "reason_ineligible": "Does not support international transactions",
                }
            )
            continue

        #  reward calculation 
        monthly_rewards = {c: 0.0 for c in categories}
        rules = list(card.reward_categories.all())

        for r in rules:
            cat = r.category
            if cat not in monthly_rewards:
                continue

            reward = monthly_reward(
                monthly_spend.get(cat, 0),
                r.reward_rate,
                getattr(r, "cap_type", "none"),
                getattr(r, "monthly_cap_amount", None),
            )
            monthly_rewards[cat] += reward

        annual_rewards_by_cat = {k: round(v * 12, 2) for k, v in monthly_rewards.items()}
        total_rewards = round(sum(annual_rewards_by_cat.values()), 2)

        # lounge value 
        lounge_value = card.lounge_visits_per_year * LOUNGE_VALUE_PER_VISIT

        #  forex cost 
        if card.supports_forex:
            forex_cost = round(monthly_foreign * 12 * (card.forex_markup_percent / 100), 2)
        else:
            forex_cost = 0.0

        # fee logic 
        fee = float(card.annual_fee)
        fee_waived = False

        if fee == 0:
            fee_waived = True
        elif card.fee_waiver_spend and annual_spend >= card.fee_waiver_spend:
            fee = 0.0
            fee_waived = True

        #  net value 
        net_value = round(total_rewards + lounge_value - fee - forex_cost, 2)

        # top category 
        top_category = max(annual_rewards_by_cat, key=annual_rewards_by_cat.get)

        eligible.append(
            {
                **meta,
                "eligible": True,
                "breakdown": annual_rewards_by_cat,
                "total_rewards": total_rewards,
                "lounge_value": round(lounge_value, 2),
                "forex_cost": forex_cost,
                "effective_fee": round(fee, 2),
                "fee_waived": fee_waived,
                "net_value": net_value,
                "top_category": top_category,
            }
        )

    if not eligible:
        return {
            "input": user_input,
            "ranked_results": [],
            "ineligible_results": ineligible,
        }

    # normalization for composite score

    cashback_vals = [c["total_rewards"] for c in eligible]
    lounge_vals = [c["lounge_value"] for c in eligible]
    fee_vals = [c["effective_fee"] for c in eligible]
    forex_vals = [c["forex_cost"] for c in eligible]
    net_vals = [c["net_value"] for c in eligible]

    cb_min, cb_max = min(cashback_vals), max(cashback_vals)
    lg_min, lg_max = min(lounge_vals), max(lounge_vals)
    fe_min, fe_max = min(fee_vals), max(fee_vals)
    fx_min, fx_max = min(forex_vals), max(forex_vals)
    nv_min, nv_max = min(net_vals), max(net_vals)

    for c in eligible:
        norm_cashback = normalize(c["total_rewards"], cb_min, cb_max)
        norm_lounge = normalize(c["lounge_value"], lg_min, lg_max)
        norm_fee = 1 - normalize(c["effective_fee"], fe_min, fe_max)
        norm_forex = 1 - normalize(c["forex_cost"], fx_min, fx_max)
        norm_net = normalize(c["net_value"], nv_min, nv_max)

        composite = (
            weights["cashback"] * norm_cashback
            + weights["lounge"] * norm_lounge
            + weights["fee"] * norm_fee
            + weights["forex"] * norm_forex
        )

        final_score = alpha * norm_net + (1 - alpha) * composite

        c["composite_score"] = round(composite, 4)
        c["final_score"] = round(final_score, 4)

    
    # ranking
    
    eligible.sort(key=lambda x: (x["net_value"], x["composite_score"]), reverse=True)

    # tie break
    ranked = []
    i = 0
    while i < len(eligible):
        group = [eligible[i]]
        j = i + 1
        while j < len(eligible) and abs(eligible[j]["net_value"] - eligible[i]["net_value"]) <= TIE_EPSILON:
            group.append(eligible[j])
            j += 1

        if len(group) > 1:
            group.sort(
                key=lambda x: (
                    x["composite_score"],
                    -x["effective_fee"],
                    x["total_rewards"],
                    x["name"],
                ),
                reverse=True,
            )

        ranked.extend(group)
        i = j

    for idx, card in enumerate(ranked, start=1):
        card["rank"] = idx

    if include_ineligible:
        for r in ineligible:
            r["rank"] = None

    return {
        "input": user_input,
        "ranked_results": ranked,
        "ineligible_results": ineligible,
    }