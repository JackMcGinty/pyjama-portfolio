from django.shortcuts import render
from django.http import HttpResponse


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