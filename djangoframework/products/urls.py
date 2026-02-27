from django.urls import path
from .api import ProductManagement,CategoryApi
from .web import ProductManaging

from .web_class import ListCategoryView
app_name = 'products'


category_api_url = [
    path('api/categories/',CategoryApi.category),
    path('api/categories/<int:id>/',CategoryApi.category_id),
]

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

web_class_url = [path('class/category/list/',ListCategoryView.as_view(), name='listcategoryclass'),]

urlpatterns = rest_api_url+web_url+web_class_url+category_api_url