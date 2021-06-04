# Stock_price

stock data can be added though post request  
/stock/add_stockdata  
with json format like  
[{'time':'2020-01-16', 'stock':'MSFT', 'open_price':4.1, 'high_price' : 4.1, 'low_price' : 4.1, 'close_price' : 4.1},  
 {'time':'2020-01-13', 'stock':'AAPL', 'open_price':4.1, 'high_price' : 4.1, 'low_price' : 4.1, 'close_price' : 4.1}]  
  
stock data can be get through symbol and time range  
example: /stock/get_stockdata?symbol=NN&start=2020-01-13&end=2020-01-14  
  
delete stock and related data based on symbol  
example: /stock/get_stockdata?symbol=MSFT  
  
test cases are written in stock/tests.py  
use python manage.py test to run test cases  
