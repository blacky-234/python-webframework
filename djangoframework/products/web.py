from django.shortcuts import render,redirect
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Category,Product,Order
from django.core.cache import cache
from django.db.models import F
from django.db import transaction
from django.core.paginator import Paginator
from django.db.models import Count,Sum,Case,When,Value,IntegerField,Q,Field,DecimalField,ExpressionWrapper,Prefetch
from django.db.models import OuterRef, Subquery,Exists
from django.db.models.functions import Coalesce



# These views only render templates. JS handles API calls.
class ProductManaging:

    def select_inventory(request):
        context = {}

        #1.category to product level grouping with annotations

        product_qs = Product.objects.annotate(
            total_value=ExpressionWrapper(F("stock") * F("price"),output_field=DecimalField()),
        )
        
        context["category_group"] = Category.objects.annotate(
                total_stock=Coalesce(Sum("products__stock"), Value(0)),
                total_inventory_value=Coalesce(Sum(F("products__stock") * F("products__price")),Value(0),output_field=DecimalField()),
                product_count=Count("products")
            ).prefetch_related(
                Prefetch("products", queryset=product_qs)
            )
        


        return render(request, "home/select_inventory.html",context)
    
    def list_category(request):
        #TODO: memcache
        # category = cache.get("category")

        # if not category:
        #     category = Category.objects.all().order_by('-id')
        #     cache.set("category", category, 60)

        category = Category.objects.all().order_by('-id')
        paginator = Paginator(category,5)
        page_no = request.GET.get('page')
        page_obj = paginator.get_page(page_no)
        return render(request, "category/list.html",{'page_obj':page_obj})
   
    @ensure_csrf_cookie
    def products_page(request):
        context = {}
        context["products"] = Product.objects.select_related("category").all()
        #TODO: Conditional Expressions and Annotations
        # category_for = Category.objects.annotate(
        #     total_products=Count("product"),
        #     total_stock=Coalesce(Sum("product__stock"),Value(0)),
        #     total_value=Coalesce(Sum(F("product__stock") * F("product__price")),Value(0),output_field=IntegerField())
        # ).all()    
     
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
    
