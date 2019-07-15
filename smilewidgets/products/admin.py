from django.contrib import admin

# Register your models here.

from .models import Product, GiftCard, ProductPrice

admin.site.register(Product)
admin.site.register(GiftCard)
admin.site.register(ProductPrice)
