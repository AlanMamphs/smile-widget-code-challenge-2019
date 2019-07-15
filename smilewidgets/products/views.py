from .models import Product
from .serializers import ProductSerializer
from .filters import ProductFilter

from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend


class ProductPriceAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        self.queryset = Product.objects.date_specific_prices(date=self.request.GET.get('date'),
                                                             gift_card_code=self.request.GET.get('giftCardCode'))
        return super().get_queryset()

    def get_serializer(self, *args, **kwargs):
        # validate date and productCode get parameter

        ProductSerializer(
            data={'date': self.request.GET.get('date'), 'code': self.request.GET.get('productCode')}).is_valid(
            raise_exception=True)
        return super().get_serializer(*args, **kwargs)
