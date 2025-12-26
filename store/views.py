from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny ,DjangoModelPermissions, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status
from .models import Product, Collection, Reviews, OrderItem, Cart, CartItem, Customer, Order
from .serializers import ProductSerializer,\
    CollectionSerializer, ReviewSerializer, \
    CartSerializer, CartItemSerializer,\
    AddCartItemSerializer, UpdateCartItemSerializer,\
    DeleteCartItemSerializer, CustomerSerializer, \
    OrderSerializer, CreateOrderSerializer,\
    UpdateOrderSerializer
from .filters import ProductFilter
from .pagination import DefaultPagination
from .permission import IsAdminOrReadOnly, ViewCustomerHistoryPermission 

# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all() 
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]       
    filterset_class = ProductFilter
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
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

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    def get_permission_classes(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated]
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request ,pk=None):
        return Response('ok')
    
    @action(detail=False ,methods=['get', 'put'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = self.get_object().get(user_id=request.user.id) # get the customer associated with the logged-in user
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)   # serialize the customer data
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data) # update the customer data
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
class OrderViewSet(ModelViewSet):
    http_method_names=['get','post','patch','delete','head','options']
    
    def get_permissions(self):
        if self.request.method in ['put','patch','delete']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self,request ,*args, **kwargs):
        serializer=CreateOrderSerializer(
            data =request.data,
            context={'user_id': self.request.user.id}
            )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT']:
            return CreateOrderSerializer
        elif self.request.method == ['patch']:
            return UpdateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user =self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id=Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id= customer_id)