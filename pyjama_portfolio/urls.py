from django.urls import path
from pyjama_portfolio import views

urlpatterns = [
    path("", views.home, name="home"),
]