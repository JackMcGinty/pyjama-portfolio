from django.shortcuts import render
from django.http import HttpResponse
from alpha_vantage.timeseries import TimeSeries

import pyjama_portfolio
ts = TimeSeries(key='RC15FSQIX0NWZDZV', output_format='pandas')
from pprint import pprint # Debug only

# Create your views here.
def home(request):
    return HttpResponse("Hello, future millionare!")
def see_stocks(request):
    return render(
        request, 
        "pyjama_portfolio/see_stocks.html",
        {
            "test_var": "donuts are good, bro",
        }
        )

def get_input(request):
    return render(
        request,
        "pyjama_portfolio/get_input.html",
    )

def display_input(request):
    get_text = "default variable"
    if request.method == "POST":
        get_text = request.POST["textfield"]
    return render(
        request,
        "pyjama_portfolio/get_input.html",
        {
            "user_input": get_text
        }
    )

def stock_search(request):
    stock_symbol = "null"
    stock_text = "default stock"
    if request.method == "POST":
        stock_symbol = request.POST["textfield"]
    if stock_symbol == "":
        return render(
            request,
            "pyjama_portfolio/see_stocks.html",
            {
                "code": "empty",
                "stock_symbol": stock_symbol,
                "stock_price": "0"
            }
        )
    try:
        data, meta_data = ts.get_daily(symbol=stock_symbol, outputsize='full')
        stock_text = data.iloc[0, 0]
    except ValueError:
	        return render(
                request,
                "pyjama_portfolio/see_stocks.html",
                {
                    "code": "invalid",
                    "stock_symbol": stock_symbol,
                    "stock_price": "0"
                }
            )
    return render(
        request,
        "pyjama_portfolio/see_stocks.html",
        {
            "code": "ok",
            "stock_symbol": stock_symbol,
            "stock_price": stock_text
        }
    )
    