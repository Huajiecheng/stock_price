from django.test import TestCase
from stock.models import Stock, StockPrice
from django.shortcuts import render, get_object_or_404
from django.core import serializers
from django.db.models import Q
import datetime
import json
from django.test import TestCase, Client
from django.http import HttpResponse, Http404, JsonResponse
from decimal import Decimal

client = Client()
class StockTest(TestCase):

    def setUp(self):
        stocks = Stock.objects.create(symbol='MSFT')
        stocks.save()
        StockPrice.objects.create(
            time = datetime.datetime.strptime("2020-01-13", '%Y-%m-%d'), stock = stocks, open_price = 1.1, high_price = 1.1, low_price = 1.1, close_price = 1.1
        )
        StockPrice.objects.create(
            time = datetime.datetime.strptime("2020-01-14", '%Y-%m-%d'), stock = stocks, open_price = 2.1, high_price = 2.1, low_price = 2.1, close_price = 2.1
        )
        StockPrice.objects.create(
            time = datetime.datetime.strptime("2020-01-15", '%Y-%m-%d'), stock = stocks, open_price = 3.1, high_price = 3.1, low_price = 3.1, close_price = 3.1
        )
    
    def test_get(self):
        response = client.get("/stock/get_stockdata?symbol=MSFT&start=2020-01-13&end=2020-01-14")
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(len(json_data), 2)

    def test_delete(self):
        response = client.get("/stock/delete_stockdata?symbol=MSFT")
        self.assertEqual(response.status_code, 204)

    def test_add(self):
        stockdata = [{'time':'2020-01-16', 'stock':'MSFT', 'open_price':4.1, 'high_price' : 4.1, 'low_price' : 4.1, 'close_price' : 4.1},
           {'time':'2020-01-13', 'stock':'AAPL', 'open_price':4.1, 'high_price' : 4.1, 'low_price' : 4.1, 'close_price' : 4.1}]
        response = client.post(
            "/stock/add_stockdata",
            data=json.dumps({"data":stockdata}),
            content_type='application/json'
        )       
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Stock.objects.all()), 2)
        self.assertEqual(len(StockPrice.objects.all()), 5)

    def test_update(self):
        stockdata = [{'time':'2020-01-15', 'stock':'MSFT', 'open_price':4.1, 'high_price' : 4.1, 'low_price' : 4.1, 'close_price' : 4.1}]
        response = client.post(
            "/stock/add_stockdata",
            data=json.dumps({"data":stockdata}),
            content_type='application/json'
        )
        updatetime = datetime.datetime.strptime('2020-01-15', '%Y-%m-%d')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(Stock.objects.all()), 1)
        self.assertEqual(len(StockPrice.objects.all()), 3)
        self.assertEqual(StockPrice.objects.get(time = updatetime).open_price, Decimal('4.10'))

    def test_get_error(self):
        response = client.get("/stock/get_stockdata?symbol=MSFT&start=2020-01-13")
        json_data = json.loads(response.content)
        self.assertEqual(response.status_code, 404)

    def test_delete_error(self):
        response = client.get("/stock/delete_stockdata?symbol=AAPL")
        self.assertEqual(response.status_code, 404)


    
        

    
