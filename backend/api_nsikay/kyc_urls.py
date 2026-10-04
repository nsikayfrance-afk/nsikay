# -*- coding: utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path("", views.kyc_status, name="kyc-status"),
]

