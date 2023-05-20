from urllib.request import urlopen
from bs4 import BeautifulSoup
from googlesearch import search


def findStock():
    #Ask what stock
    StockName = input('Enter the name of the stock you want information for: ')
    #Specify this input is a stock that exists on the nasdaq and format the input
    StockPage = "Nasdaq Stock" + StockName
    #Search the web for the first page that is returned from the given input
    StockQuote = searchStockInfo(StockPage)
    #Set the page that we will be scraping
    quote_page = StockQuote
    #Query the website and return the html to the variable 'html_page'
    html_page = urlopen(quote_page)
    #Parse the html using beautfil soup and store in the variable 'soup'
    soup = BeautifulSoup(html_page, 'html.parser')
    #Get the price
    stock_price_box = soup.find('div', attrs={'class':'qwidget-dollar'})
    #Print the price
    print(stock_price_box.text)
    return stock_price_box.text

# Currently returns the first website queried from request
# Goal: return stock acronym, price, recent news
def searchStockInfo(stockString):
    url = ""
    for url in search(stockString,num=1, start=1, stop=2):
        print(url)
    return url