from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.mixins import CreateModelMixin,DestroyModelMixin
from rest_framework.viewsets import ModelViewSet ,GenericViewSet
from rest_framework.response import Response
from rest_framework.filters import SearchFilter , OrderingFilter
from rest_framework import status
from .models import Product, Collection, Reviews, OrderItem, Cart,CartItem
from .serializers import ProductSerializer,\
    CollectionSerializer, ReviewSerializer, \
    CartSerializer,CartItemSerializer,\
    AddCartItemSerializer, UpdateCartItemSerializer,\
    DeleteCartItemSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]       
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']


    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Gusubira ntabwo bikunze'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        product_count=Count('products')
    ).all()
    serializer_class = CollectionSerializer
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:  # Changed from ProductItem
            return Response({'error': 'Gusubira ntabwo bikunze'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)   

class ReviewsViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Reviews.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

class CartViewSet(CreateModelMixin, GenericViewSet, DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class cartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        elif self.request.method == 'DELETE':
            return DeleteCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects\
            .filter(cart_id=self.kwargs['cart_pk'])\
            .select_related('product')
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}