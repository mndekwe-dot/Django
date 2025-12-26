from django.contrib import admin , messages
from django.db.models import Count
from django.utils.html import format_html, urlencode   
from django.urls import reverse
from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)

# Register your models here.

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields ={
        'slug' : ['title']
    }
    actions = ['clear_inventory']  # to add custom action
    list_display = ['title', 'unit_price', 'inventory_status','collection_title'] # to show inventory status instead of inventory field
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection'] # to optimize queries by using select_related for foreign key

    def collection_title(self, product): # custom method to show collection title
        return product.collection.title

    @admin.display(ordering='inventory') # to sort by inventory column
    def inventory_status(self, product): # custom method to show inventory status
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    @admin.action(description='Clear inventory') # custom action to clear inventory
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.SUCCESS
        )

@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name','membership','orders_count']
    list_editable = ['membership']
    list_filter = ['membership', 'order__placed_at', InventoryFilter]
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (
            reverse('admin:store_order_changelist') 
            + '?' 
            + urlencode({'customer__id': str(customer.id)})
        )
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')  
        )
    

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        urls = (
            reverse('admin:store_product_changelist') 
            + '?' 
            + urlencode({'collection__id': str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', urls,collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 10

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at', 'customer']
    list_per_page = 10
    autocomplete_fields = ['customer']