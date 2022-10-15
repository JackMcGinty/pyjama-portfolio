# PyjamaPortfolio
![a snake trading stocks](./snake-stocks2-big.jpeg)  
(Craiyon.com, prompt = "a snake trading stocks professional high quality")


## Overview

Want to trade stocks, but haven't got the time, knowledge, or money?<br/>
Welcome to PyjamaPortfolio.  
It will probably won't help much with the time or knowledge, but it will allow you to learn how to play the market without all the bother of hiring a stockbroker, buying a fancy suit, or potentially losing your life's savings when the economy crashes.  

### The name is cool, but why?
As you no doubt know, people from England, Canada, and other blighted localities spell "Pajamas" (as in the things you wear while sleeping) with a y: "Pyjamas". I use this spelling because the app is written in Django, a Python framework (**py**jamas = **py**thon).


### How it works
This app uses real-time stock data (obtained through an API called [AlphaVantage](https://www.alphavantage.co/)) to allow the user to 'buy' and 'sell' stocks. The quotes here are important because there is no actual money involved. Instead, an arbitrarily-set number in a database goes up or down by an amount equal to the current stock price. This allows the user to practiace 'playing the market', gaining the instincts and experience which are critical to successful investing.

To start the test server, you need Django installed. I haven't actually tested the portability of this code, so this might not work. After you have installed Django and Pandas (the API call requires it to format the return value) in a virtual environment, you open a terminal and run:  
`python manage.py runserver`  
You may have to replace `python` with the name of your python installation, depending on your OS. Personally, I just added a zsh alias to make `python` synonomous with `python3`.  
If the command executed correctly, you should get a line saying something like:  
`Starting development server at http://127.0.0.1:8000/`  
If you hold down the control key and click this link, you will be taken to a web page representing the contents of the local server. In the case of this app, this is a crusty home page with some links that will take you to the other parts of the app.  
The stock buying page lets you buy stocks, and the portfolio viewing page lets you sell them.  
The stocks you buy are stored in a sqlite3 database, as is your financial balance (i.e. your arbitrary and meaningless number representing money).

I made this web app for two reasons: 
1. I've been wanting to make a stock simulator for some time (about three weeks)
1. I've never made a Django app before
I've worked briefly with Node, but I've always wanted to give Django a try because I'm more familiar with Python than with JavaScript and thought I could implement more advanced features more easily.

Here's a video of me demoing the software:  
[Stock trading in action](https://youtu.be/JGZ7tjp87N4)

## Web Pages
The Home page is the one which first greets the user. It isn't very exciting, and doesn't even count towards the requirements of this project because it isn't dynamically generated.<br/>
The see_stocks page is where the user can search for and buy stocks. The stock price is obtained through an API call and dynamically generated on each search. There's some basic error checking here in case you enter a stock that doesn't exist. When a stock is successfully found, a "purchase" button appears, which (when clicked) will add the stock to the database which represents your portfolio. A link at the bottom takes them to the view_portfolio page.<br/>
The view_portfolio page allows the user to see their current stock collection and sell bits of it off at the current market price. The portfolio is (of course) generated dynamically based on what stocks the user has bought. A link at the bottom will take them back to the stock buying screen.<br/>
A navigation bar pervades the website, allowing the user to switch between any of the pages at will.

## Development Environment
This project was written entirely in VSCode. Heavy use was made of the Django, Python, Pylance, HTML, and CSS extensions.  
A virtual environment was used to handle the libraries required for this project.
As a web app, HTML and CSS were involved in the project, but the dynamic side was handled entirely by Python.

## Useful Websites
* [PythonHow.com](https://pythonhow.com/python-tutorial/pandas/Accessing-pandas-dataframe-columns-rows-and-cells/)
* [Alphavantage.co Documentation](https://www.alphavantage.co/documentation/)
* [Alphavantage Python Wrapper](https://github.com/RomelTorres/alpha_vantage)
* [RealPython](https://realpython.com/python-api/)
* [StackOverflow, specifically the linked thread](https://stackoverflow.com/questions/25028895/very-simple-user-input-in-django)
* [Django forums, specifically the linked thread](https://forum.djangoproject.com/t/read-which-button-in-a-loop-was-clicked/648/5)

## Future Work
* Make it look less crusty (i.e. add some CSS)
* Make it run on an actual server so I (and other people) can access it without having to run a dev server
* Make it possible to buy / sell quantities of stocks, instead of multiple shares of the same company one at a time