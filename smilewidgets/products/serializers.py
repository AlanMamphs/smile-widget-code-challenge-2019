from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    my_default_errors = {
        'required': 'Please include productCode in get parameters',
        'blank': 'Please include productCode in get parameters'
    }
    price = serializers.SerializerMethodField('get_date_specific_price', read_only=True)
    name = serializers.CharField(read_only=True)

    # write only to check get params
    date = serializers.DateField(write_only=True)
    code = serializers.CharField(write_only=True, error_messages=my_default_errors)

    class Meta:
        model = Product
        fields = ('price', 'id', 'name', 'date', 'code')

    @staticmethod
    def get_date_specific_price(obj):
        return obj.new_price if obj.new_price > 0 else 0