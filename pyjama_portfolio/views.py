from multiprocessing.sharedctypes import Value
from django.shortcuts import render
from django.http import HttpResponse
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime, date
import sqlite3
from pytz import timezone
ts = TimeSeries(key='RC15FSQIX0NWZDZV', output_format='pandas')

# So we don't have to constantly run API queries
global_stock_price = 0.0

# So other functions can access data entered on the website once
global_stock_symbol = ""


# Create your views here.
def home(request):
    return render(
        request,
        "pyjama_portfolio/homepage.html",
    )


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
    global global_stock_price, global_stock_symbol
    stock_symbol = ""
    stock_text = "default stock"
    if request.method == "POST":
        stock_symbol = request.POST["textfield"].upper()
    if stock_symbol == "":
        return render(
            request,
            "pyjama_portfolio/see_stocks.html",
            {
                "money": get_funds(),
                "code": "empty",
                "stock_symbol": stock_symbol,
                "stock_price": "0"
            }
        )
    try:
        data, meta_data = ts.get_daily(symbol=stock_symbol, outputsize='full')
        stock_text = data.iloc[0, 3]
    except ValueError:
	        return render(
                request,
                "pyjama_portfolio/see_stocks.html",
                {
                    "money": get_funds(),
                    "code": "invalid",
                    "stock_symbol": stock_symbol,
                    "stock_price": "0"
                }
            )
    global_stock_price = float(stock_text)
    global_stock_symbol = stock_symbol
    return render(
        request,
        "pyjama_portfolio/see_stocks.html",
        {
            "money": get_funds(),
            "code": "ok",
            "stock_symbol": stock_symbol,
            "stock_price": stock_text
        }
    )

def buy_stock(request):
    global global_stock_price, global_stock_symbol
    if global_stock_symbol == "":
        return render(
            request,
            "pyjama_portfolio/see_stocks.html",
            {
                "money": get_funds(),
                "code": "empty",
                "stock_symbol": global_stock_symbol,
                "stock_price": "0"
            }
        )
    # Connect to Database
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    # Create the stocks table (assuming we haven't already)
    cursor.execute("CREATE TABLE IF NOT EXISTS stocks (symbol TEXT, purchased_date DATE, bought_price REAL, secondary_id INTEGER)")
    # Insert the data
    try:
        values = (
            global_stock_symbol,
            date.fromtimestamp(datetime.now(timezone('US/Mountain')).timestamp()), 
            global_stock_price,
            len(query_portfolio())
        )
        cursor.execute("INSERT INTO stocks VALUES (?,?,?,?)", values)
        connection.commit()
        print("Successfully bought a share")
    except ValueError:
        print(f"error inserting {global_stock_symbol} into portfolio")
    connection.close()
    update_funds(-global_stock_price)
    return render(
            request,
            "pyjama_portfolio/see_stocks.html",
            {
                "money": get_funds(),
                "code": "empty",
                "stock_symbol": global_stock_symbol,
                "stock_price": "0"
            }
        )

def get_funds():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM funds")
    funds = 0.0
    # Refactor here
    results = cursor.fetchall()
    if len(results) == 0:
        print("there's nothing here!!!")
        return 0.0
    funds = round(results[0][0], 2)
    print(f"funds should be {results[0][0]}")
    
    connection.close()
    return funds

# We need the connection here so we can commit
def update_funds(amount: float):
    print(f"Funds were updated by {amount}")
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("UPDATE funds SET balance = balance + ?", (amount,))
    connection.commit()
    connection.close()

def initiate_funds(starting_balance: float):
    print("initiating funds table")
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    # Drop and create the funds table.
    # Note: the drop here is for Debugging only!
    cursor.execute("DROP TABLE IF EXISTS funds") # Remove after release
    cursor.execute("CREATE TABLE IF NOT EXISTS funds (balance REAL)")
    cursor.execute("INSERT INTO funds VALUES (?)", (starting_balance,))
    connection.commit()
    connection.close()

# Starting balance:
initiate_funds(50.00)

def view_portfolio(request):
    portfolio = query_portfolio()
    return render(
        request,
        "pyjama_portfolio/view_portfolio.html",
        {
            "money": get_funds(),
            "portfolio": portfolio,
            "stock_symbol": portfolio,
        }
    )

def query_portfolio() -> list:
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    # Obtain the data
    cursor.execute("SELECT * FROM stocks")
    results = cursor.fetchall()
    connection.close()
    if len(results) == 0:
        return []
    return results

def sell_stock(request):
    which_stock = 0
    stock_price = 0.0
    if request.method == "POST":
        which_stock = request.POST["stock_id"]
    # Obtain the stock information
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM stocks WHERE secondary_id = ?", (which_stock,))
    result = cursor.fetchall() # should only return one
    # Query AlphaVantage for current price
    try:
        data, meta_data = ts.get_daily(symbol=result[0][0], outputsize='full')
        stock_price = data.iloc[0, 3]
    except ValueError:
        print("Something went wrong")
        portfolio = query_portfolio()
        connection.close()
        return render(
            request,
            "pyjama_portfolio/view_portfolio.html",
            {
                "money": get_funds(),
                "portfolio": portfolio,
                "stock_symbol": portfolio,
            }
        )
    update_funds(+stock_price)
    cursor.execute(f"DELETE FROM stocks WHERE secondary_id = {which_stock}")
    connection.commit()
    connection.close()
    portfolio = query_portfolio()
    return render(
        request,
        "pyjama_portfolio/view_portfolio.html",
        {
            "money": get_funds(),
            "portfolio": portfolio,
            "stock_symbol": portfolio,
        }
    )

# CAUTION!!!!!!
#   This function is to be used in debugging ONLY!
#   Do not allow access from the general public!!!!
def wipe_stocks():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS stocks")
    connection.commit()
    connection.close()
