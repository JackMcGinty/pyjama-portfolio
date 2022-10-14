from django.urls import path
from pyjama_portfolio import views

urlpatterns = [
    path("", views.home, name="home"),
    path("see_stocks/", views.see_stocks, name="see_stocks"),
    path("get_input/", views.get_input, name="get_input"),
    path("stock_search/", views.stock_search, name="stock_search"),
    path("buy_stock/", views.buy_stock, name="buy_stock")
]