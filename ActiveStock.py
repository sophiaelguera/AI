from googlesearch import search
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Create a list to hold the urls of our stocks
stock_list = []
# Looks for the most active stocks of the days and pulls their price from their NASDAQ page with StockPrice() function
def findMostActiveStocks():
    activeStocks = "https://ojp.nationalrail.co.uk/service/timesandfares/NRW/CST/today/1215/dep"
    #Set the page that we will be scraping
    quote_page = activeStocks
    #Query the website and return the html to the variable 'html_page'
    html_page = urlopen(quote_page)
    #Parse the html using beautfil soup and store in the variable 'soup'
    soup = BeautifulSoup(html_page, 'html.parser')
    #Get the price
    stock_price_box = soup.find_all('a', attrs={'class':'mostactive'})
    for n in stock_price_box:
        stock_list.append(n.attrs['href'])

    # List top 10 traded stocks
    for i in range(10):
        print(stock_list[i])
        print(getStockPrice(stock_list[i]))
        print("---------------")

    # Prints an array of all the NASDAQ urls of the most active stocks
    #print(stock_list)


def getStockPrice(stockName):
    #Query the website and return the html to the variable 'html_page'
    html_page = urlopen(stockName)
    #Parse the html using beautfil soup and store in the variable 'soup'
    soup = BeautifulSoup(html_page, 'html.parser')
    #Get the price
    stock_price_box = soup.find('div', attrs={'class':'qwidget-dollar'})
    #Print the price
    return "Price: " + stock_price_box.text