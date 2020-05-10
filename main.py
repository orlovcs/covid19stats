"""
Primary driver.
"""
#selenium
from selenium import webdriver


#pandas
import pandas as pd

from stocks import Stock

stock_list = []

driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver', )
driver.get("https://finance.yahoo.com/gainers")
result = driver.page_source #load entire page
assert "Stock" in driver.title

tbody = driver.find_element_by_tag_name("tbody")
for row in tbody.find_elements_by_tag_name("tr"):
    cells = row.find_elements_by_tag_name("td")
    symbol = cells[0].text
    name = cells[1].text
    price = cells[2].text
    change = cells[3].text
    percent_change = cells[4].text
    stock_list.append(Stock(symbol, name, price, change, percent_change))

top_names = []
top_symbols = []
top_price = []
top_change = []
top_percent_change = []

for top_stock in stock_list[:5]:
    top_names.append(top_stock.name)
    top_symbols.append(top_stock.symbol)
    top_price.append(top_stock.price)
    top_change.append(top_stock.change)
    top_percent_change.append(top_stock.percent_change)

data_top_5 = {
    'Name': top_names,
    'Symbol':top_symbols,
    'Price':top_price,
    'Change':top_change,
    'Change (%)':top_percent_change
}

df = pd.DataFrame(data_top_5, columns=['Name', 'Symbol', 'Price', 'Change', 'Change (%)'])
print(df)
driver.close()
