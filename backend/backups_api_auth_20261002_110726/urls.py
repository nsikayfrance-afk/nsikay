
from django.urls import path
from . import views

urlpatterns=[

path("users/",views.users),
path("banks/",views.banks),
path("countries/",views.countries),
path("certifications/",views.certifications),
path("transactions/",views.transactions),
path("finance/",views.finance),

]
