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