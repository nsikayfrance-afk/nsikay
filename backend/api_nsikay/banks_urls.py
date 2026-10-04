# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path("", views.banks_list, name="banks-list"),
]

