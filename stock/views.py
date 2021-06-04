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
	if request.method == "POST":
		json_data = json.loads(request.body)['data']		
		for record in json_data:
			if Stock.objects.filter(symbol = record['stock']).exists():
				stocks = Stock.objects.get(symbol = record['stock'])
			else:
				stocks = Stock(symbol = record['stock'])
				stocks.save()
			try:
				record_time = datetime.datetime.strptime(record['time'], '%Y-%m-%d')
			except ValueError:
				return HttpResponse("Wrong time format",status=404)
			if StockPrice.objects.filter(Q(stock=stocks) & Q(time=record_time)).exists():
				StockPrice.objects.filter(Q(stock=stocks) & Q(time=record_time)).update(open_price = float(record['open_price']), 
					high_price = float(record['high_price']), low_price = float(record['low_price']), close_price = float(record['close_price']))
			else:
				prices = StockPrice(time = record_time, stock = stocks, open_price = float(record['open_price']), 
					high_price = float(record['high_price']), low_price = float(record['low_price']), close_price = float(record['close_price']))
				prices.save()
		return HttpResponse("Successully add stock data", status = 201)

# get json data based on symbol and time range
# example: http://127.0.0.1:8000/stock/get_stockdata?symbol=NN&start=2020-01-13&end=2020-01-14
def get_data(request):
	if request.method == "GET":
		if 'symbol' in request.GET:
			item = get_object_or_404(Stock, symbol=request.GET["symbol"])
		else:
			return HttpResponse("Missing symbol parameter", status=404)
		if 'start' in request.GET and 'end' in request.GET:
			try:
				start_time = datetime.datetime.strptime(request.GET["start"], '%Y-%m-%d')
				end_time = datetime.datetime.strptime(request.GET["end"], '%Y-%m-%d')
			except ValueError:
				return HttpResponse("Wrong time format",status=404)
			item = get_object_or_404(Stock, symbol=request.GET["symbol"])
			data = StockPrice.objects.filter(Q(stock=item) & Q(time__range=[start_time, end_time])).order_by("time")
			context = serializers.serialize("json", data) 
			context = json.loads(context)
			return JsonResponse(context, safe = False)
		else:
			return HttpResponse("Missing time range parameter",status=404)

#delete stock and related data based on symbol
def delete_data(request):
	if request.method == "GET":
		if 'symbol' in request.GET:
			item = get_object_or_404(Stock, symbol=request.GET["symbol"])
			item.delete()
			return HttpResponse("successully delete", status =204)
		else:
			return HttpResponse("No symbol parameter",status=404)