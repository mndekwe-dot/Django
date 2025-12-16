from django_filters.rest_framework import filterset
from .models import Product

class ProductFilter(filterset.FilterSet):
    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt'],
        }