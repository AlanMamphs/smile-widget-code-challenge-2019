from rest_framework.test import APITestCase
from products.models import Product, GiftCard, ProductPrice
from django.urls import reverse


class GetPriceViewTest(APITestCase):

    def setUp(self):
        self.url = reverse('get-price')
        self.product = Product.objects.create(name='Big Widget', code='big_widget', price=100000)
        self.giftcard = GiftCard.objects.create(code="10OFF", amount=1000, date_start="2018-07-01", date_end=None)
        self.big_giftcard = GiftCard.objects.create(code="1000OFF", amount=1000000, date_start="2018-07-01",
                                                    date_end=None)
        self.black_friday = ProductPrice.objects.create(title="Black Friday",
                                                        product=self.product,
                                                        price=30000,
                                                        date_start="2019-11-23",
                                                        date_end="2019-11-25")
        self.price2019 = ProductPrice.objects.create(title="Black Friday",
                                                     product=self.product,
                                                     price=40000,
                                                     date_start="2019-01-01",
                                                     date_end="2019-12-01")

    @staticmethod
    def total(event_price, gift_amount):
        if event_price - gift_amount > 0:
            return event_price - gift_amount
        return 0

    def test_get_price(self):
        # Test url parameters absence failure
        response = self.client.get(self.url)
        self.assertEqual(400, response.status_code)

        response = self.client.get(self.url, data={'productCode': "big_widget", "date": "2018-12-12"})
        self.assertEqual(200, response.status_code)
        self.assertTrue(len(response.data) > 0)

        # Test against adjusted price.
        # Test that price changes to minimum of two adjusted price

        response = self.client.get(self.url, data={'productCode': "big_widget", "date": "2019-11-23"})
        self.assertTrue(
            response.data[0]['price'] == self.black_friday.price if self.black_friday.price < self.price2019.price
            else response.data[0]['price'] == self.price2019.price)

        # Test against added gift.
        # Test that price changes if gift code is added

        response = self.client.get(self.url,
                                   data={'productCode': "big_widget", "date": "2019-11-23", "giftCardCode": "10OFF"})

        self.assertTrue(response.data[0]['price'] == self.total(self.black_friday.price, self.giftcard.amount)
                        if self.black_friday.price < self.price2019.price
                        else response.data[0]['price'] == self.total(self.price2019.price, self.giftcard.amount))

        # Test against huge gift.
        # Test that price sets to 0 if price is negative

        response = self.client.get(self.url,
                                   data={'productCode': "big_widget", "date": "2019-11-23", "giftCardCode": "1000OFF"})

        self.assertTrue(
            response.data[0]['price'] == self.total(self.black_friday.price, self.big_giftcard.amount)
            if self.black_friday.price < self.price2019.price
            else response.data[0]['price'] == self.total(self.price2019.price, self.big_giftcard.amount))
