from django.db import models

class Stock(models.Model):
	symbol = models.CharField(max_length=20, unique=True)

	def __str__(self):
		return 'Stock' + str(self.id)

class StockPrice(models.Model):
	time = models.DateTimeField()
	stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name = "price")
	open_price = models.DecimalField(max_digits = 20, decimal_places = 2)
	high_price = models.DecimalField(max_digits = 20, decimal_places = 2)
	low_price = models.DecimalField(max_digits = 20, decimal_places = 2)
	close_price = models.DecimalField(max_digits = 20, decimal_places = 2)

	def __str__(self):
		return 'StockPrice' + str(self.id)


