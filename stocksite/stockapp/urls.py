from django.urls import path
from . import views

urlpatterns = [
    path("", views.sourcepage, name="sourcepage"),
    path("homepage", views.homepage, name="homepage"),
    path("results", views.results, name="results"),
    path("comparison", views.comparison, name="comparison"),
    path("sentimentanalysis", views.sentimentanalysis, name="sentimentanalysis"),
    path("testing", views.testing,name="testing")
]