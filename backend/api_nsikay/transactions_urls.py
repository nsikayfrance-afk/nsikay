# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path("", views.transactions_list, name="transactions-list"),
]

