from django_filters import rest_framework
from .models import Product


class ProductFilter(rest_framework.FilterSet):
    productCode = rest_framework.CharFilter(field_name='code')

    class Meta:
        model = Product
        fields = ['productCode']
