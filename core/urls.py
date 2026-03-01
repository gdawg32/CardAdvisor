from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("analyze/", card_input_view, name="card_input"),
]