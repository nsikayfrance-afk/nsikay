# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path("", views.wallet_dashboard, name="wallet-dashboard"),
]

