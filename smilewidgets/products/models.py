from django.db import models
from django.db.models import Q, When, ExpressionWrapper, Case, F, Min, Aggregate
import datetime


class ProductManager(models.Manager):
    """ Custom manager to query adjusted price related object """

    def date_specific_prices(self, date=None, gift_card_code=None):
        qs = self.get_queryset()
        if not date:
            date = datetime.datetime.now().date()

        gift_card = None

        if gift_card_code:
            gift_card = GiftCard.objects.get_date_specific_giftcard(date=date, code=gift_card_code)

        gift_card_amount = gift_card.amount if gift_card else 0

        date_query = Q(new_product_price__date_start__lte=date) & Q(new_product_price__date_end__gte=date)

        date_price_expr = When(date_query,
                               then=F('new_product_price__price') - gift_card_amount)

        date_price_exist_expr = When(date_query,
                                     then=True)

        qs = qs.annotate(new_price_exist=Case(date_price_exist_expr,
                                              default=False,
                                              output_field=models.BooleanField()),
                         new_price=Case(date_price_expr,
                                        default=F('price'),
                                        output_field=models.IntegerField())).order_by('pk',
                                                                                      '-new_price_exist').distinct('pk')

        return qs


class GiftCardManager(models.Manager):
    def get_date_specific_giftcard(self, code, date):
        gift_card = GiftCard.objects.filter(Q(code=code) & Q(date_start__lte=date) &
                                            (Q(date_end__gte=date) | Q(
                                                date_end__isnull=True))).first()

        return gift_card


class Product(models.Model):
    name = models.CharField(max_length=25, help_text='Customer facing name of product')
    code = models.CharField(max_length=10, help_text='Internal facing reference to product')
    price = models.PositiveIntegerField(help_text='Price of product in cents')

    objects = ProductManager()

    def __str__(self):
        return '{} - {}'.format(self.name, self.code)


class GiftCard(models.Model):
    code = models.CharField(max_length=30)
    amount = models.PositiveIntegerField(help_text='Value of gift card in cents')
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)

    objects = GiftCardManager()

    def __str__(self):
        return '{} - {}'.format(self.code, self.formatted_amount)

    @property
    def formatted_amount(self):
        return '${0:.2f}'.format(self.amount / 100)


class ProductPrice(models.Model):
    title = models.CharField(max_length=200, help_text='Helpful title for differentiating prices')
    product = models.ForeignKey(to='Product', on_delete=models.CASCADE, related_name='new_product_price')
    price = models.PositiveIntegerField(help_text='Price of products in cents')
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return '{} - {} - {}'.format(self.product, self.price, self.title)
