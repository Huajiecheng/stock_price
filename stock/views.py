from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.db.models import Q
import datetime
import json
from django.http import HttpResponse, Http404, JsonResponse
from stock.models import Stock,StockPrice
from asgiref.sync import sync_to_async

# add or update stock data
def add_data(request):
	if request.method == "GET":
		if Stock.objects.filter(symbol ="NN").exists():
			stocks = Stock.objects.get(symbol = "NN")
		else:
			stocks = Stock(symbol = "NN")
			stocks.save()
		prices = StockPrice(time = datetime.datetime.strptime("2020-01-13", '%Y-%m-%d'), stock = stocks, open_price = 1.1, high_price = 1.1, low_price = 1.1, close_price = 1.1)
		prices.save()
		return HttpResponse("Successully add stock data")

# get json data based on symbol and time range
# example: http://127.0.0.1:8000/stock/get_stockdata?symbol=NN&start=2020-01-13&end=2020-01-14
async def get_data(request):
	if request.method == "GET":
		if 'symbol' in request.GET:
			item = get_object_or_404(Stock, symbol=request.GET["symbol"])
		else:
			return HttpResponse("Missing symbol parameter")

		if 'start' in request.GET and 'end' in request.GET:
			try:
				start_time = datetime.datetime.strptime(request.GET["start"], '%Y-%m-%d')
				end_time = datetime.datetime.strptime(request.GET["end"], '%Y-%m-%d')
			except ValueError:
				return HttpResponse("Wrong time format")
			data = StockPrice.objects.filter(Q(stock=item) & Q(time__range=[start_time, end_time])).order_by("time")
			context = serializers.serialize("json", data) 
			context = json.loads(context)
			return JsonResponse(context, safe = False)
		else:
			return HttpResponse("Missing time range parameter")

#delete stock and related data based on symbol
def delete_data(request):
	if request.method == "GET":
		if 'symbol' in request.GET:
			item = get_object_or_404(Stock, symbol=request.GET["symbol"])
			item.delete()
			return HttpResponse("successully delete")
		else:
			return HttpResponse("No symbol parameter")