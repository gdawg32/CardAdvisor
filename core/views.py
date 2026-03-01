from django.shortcuts import render
from core.services.decision_engine import evaluate_cards

# Create your views here.

def index(request):
    return render(request, "index.html")

def card_input_view(request):
    if request.method == "POST":

        def get_float(name, default=0):
            try:
                return float(request.POST.get(name) or default)
            except:
                return default

        data = {
            "online": get_float("online"),
            "fuel": get_float("fuel"),
            "dining": get_float("dining"),
            "travel": get_float("travel"),
            "groceries": get_float("groceries"),
            "other": get_float("other"),
            "monthly_foreign": get_float("monthly_foreign"),
            "annual_income": get_float("annual_income"),
            "fee_tolerance": get_float("fee_tolerance", None),
        }

        weights = {
            "cashback": get_float("weight_cashback", 0.6),
            "lounge": get_float("weight_lounge", 0.2),
            "fee": get_float("weight_fee", 0.15),
            "forex": get_float("weight_forex", 0.05),
        }

        payload = evaluate_cards(data, weights=weights)

        results = payload["ranked_results"]
        top_card = results[0] if results else None

        return render(
            request,
            "results.html",
            {
                "input": data,
                "results": results,
                "top_card": top_card,
            },
        )

    return render(request, "input.html")