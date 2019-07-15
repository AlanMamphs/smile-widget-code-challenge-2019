from django.urls import path
from .views import ProductPriceAPIView

urlpatterns = [
    path('get-price', ProductPriceAPIView.as_view(), name='get-price'),
]