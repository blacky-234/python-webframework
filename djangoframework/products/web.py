from django.shortcuts import render,redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Category,Product,Order
from django.core.cache import cache
from django.db.models import F
from django.db import transaction



# These views only render templates. JS handles API calls.
class ProductManaging:

    def select_inventory(request):
        return render(request, "home/select_inventory.html")
    
    def list_category(request):
        #TODO: memcache
        # category = cache.get("category")

        # if not category:
        #     category = Category.objects.all().order_by('-id')
        #     cache.set("category", category, 60)

        category = Category.objects.all().order_by('-id')
        return render(request, "category/list.html",{"categories":category})
   
    @ensure_csrf_cookie
    def products_page(request):
        context = {}
        context["products"] = Product.objects.select_related("category").all()
        return render(request, "product.html",context)

    @ensure_csrf_cookie
    def product_form_page(request):
        if request.method == "GET":
            context = {}
            context["categories"] = Category.objects.all()
            return render(request, "products/addProduct_form.html",context)
        elif request.method == "POST":
            name = request.POST.get("productname")
            price = request.POST.get("productprice")
            stock = request.POST.get("productstock")
            category = request.POST.get("productcategory")

            Product.objects.create(name=name,price=price,stock=stock,category_id=category)

            return redirect("products:listproducts")
        

    
    def orders_page(request):
        if request.method == "GET":
            context = {}
            if request.method == "GET":
                context["orders"] = Order.objects.select_related("product","product__category").all()
                print("orders: ",context["orders"])
                return render(request, "order/orderhome.html",context)
    
    def order_form_page(request):
        context = {}
        if request.method == "GET":
            context["products"] = Product.objects.all().values("id","name")
            print("product names: ",context["products"])
            return render(request, "order/addorderform.html",context)
        elif request.method == "POST":
            product = request.POST.get("productid")
            quantity = request.POST.get("productquantity")

            #Using Atomic Transaction
            with transaction.atomic():
                product = Product.objects.select_for_update().get(id=product)
                if product.stock < int(quantity):
                    return redirect("products:orderspage")
                
                product.stock = F("stock") - int(quantity)
                product.save()
                product.refresh_from_db()

                total_price = product.price * int(quantity)
                Order.objects.create(product=product,qty=quantity,total=total_price)
            return redirect("products:orderspage")
    
