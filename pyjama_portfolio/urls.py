from django.urls import path
from pyjama_portfolio import views

urlpatterns = [
    path("", views.home, name="home"),
    path("see_stocks/", views.see_stocks, name="see_stocks"),
    path("get_input/", views.get_input, name="get_input"),
    path("display_input/", views.display_input, name="display_input"),
]