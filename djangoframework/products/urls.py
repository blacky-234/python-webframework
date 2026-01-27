from django.urls import path
from .api import ProductManagement
from .web import ProductManaging

app_name = 'products'

rest_api_url = [
    path('management/',ProductManagement.product_management, name='productmanagement'),
    path('add/category/',ProductManagement.create_category, name='createcategory'),
    path('add/product/',ProductManagement.create_product, name='createproduct'),
    path('add/order/',ProductManagement.create_order, name='createorder'),
]

web_url = [

    path('',ProductManaging.select_inventory, name='selectinventory'),
    path('category/list/',ProductManaging.list_category, name='listcategory'),
    path('list/',ProductManaging.products_page, name='listproducts'),
    path('add/form',ProductManaging.product_form_page, name='productform'),
    path('orders/',ProductManaging.orders_page, name='orderspage'),
    path('add/order/form/',ProductManaging.order_form_page, name='addorderform'),
]

urlpatterns = rest_api_url+web_url