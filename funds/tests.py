from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from datetime import date
from .models import Fund

class FundModelTest(TestCase):
    def test_fund_creation(self):
        fund = Fund.objects.create(
            name="Test Fund",
            strategy="Long/Short Equity",
            aum=Decimal('1000000'),
            inception_date=date(2020, 1, 1)
        )
        self.assertEqual(fund.name, "Test Fund")
        self.assertEqual(fund.strategy, "Long/Short Equity")
        self.assertEqual(fund.aum, Decimal('1000000'))

class FundViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        Fund.objects.create(
            name="Test Fund 1",
            strategy="Long/Short Equity",
            aum=Decimal('1000000')
        )
        Fund.objects.create(
            name="Test Fund 2",
            strategy="Global Macro",
            aum=Decimal('2000000')
        )

    def test_fund_list_view(self):
        response = self.client.get(reverse('fund_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Fund 1")
        self.assertContains(response, "Test Fund 2")

    def test_fund_filtering(self):
        response = self.client.get(reverse('fund_list'), {'strategy': 'Long/Short Equity'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Fund 1")
        self.assertNotContains(response, "Test Fund 2")

class FundAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.fund = Fund.objects.create(
            name="API Test Fund",
            strategy="Arbitrage",
            aum=Decimal('500000')
        )

    def test_api_fund_list(self):
        response = self.client.get(reverse('api_fund_list'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['funds']), 1)
        self.assertEqual(data['funds'][0]['name'], "API Test Fund")

    def test_api_fund_detail(self):
        response = self.client.get(reverse('api_fund_detail', args=[self.fund.id]))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['name'], "API Test Fund")
