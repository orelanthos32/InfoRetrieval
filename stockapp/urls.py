from django.urls import path
from . import views

urlpatterns = [
    path("", views.sourcepage, name="sourcepage"),
    path("homepage", views.homepage, name="homepage"),
    path("results", views.results, name="results"),
    path("words", views.words, name="words")
]