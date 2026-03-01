from django.db import models


class CreditCard(models.Model):
    name = models.CharField(max_length=100)
    issuer = models.CharField(max_length=100)

    annual_fee = models.PositiveIntegerField(default=0)
    fee_waiver_spend = models.PositiveIntegerField(
        help_text="Annual spend required to waive fee", default=0
    )

    lounge_visits_per_year = models.PositiveIntegerField(default=0)

    supports_forex = models.BooleanField(
    default=True,
    help_text="Whether the card supports international transactions"
    )

    forex_markup_percent = models.FloatField(
        help_text="Forex markup percentage", default=0.0
    )

    min_income_required = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
class RewardCategory(models.Model):
    CATEGORY_CHOICES = [
        ("online", "Online"),
        ("fuel", "Fuel"),
        ("dining", "Dining"),
        ("travel", "Travel"),
        ("groceries", "Groceries"),
        ("other", "Other"),
    ]

    CAP_TYPE_CHOICES = [
        ("none", "No Cap"),
        ("spend", "Spend Cap"),
        ("cashback", "Cashback Cap"),
    ]

    card = models.ForeignKey(
        CreditCard,
        on_delete=models.CASCADE,
        related_name="reward_categories",
    )

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    reward_rate = models.FloatField(
        help_text="Cashback rate (e.g., 0.05 for 5%)"
    )

    cap_type = models.CharField(
        max_length=10,
        choices=CAP_TYPE_CHOICES,
        default="none"
    )

    monthly_cap_amount = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Cap value: spend or cashback depending on cap_type"
    )

    def __str__(self):
        return f"{self.card.name} - {self.category}"