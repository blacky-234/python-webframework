from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics,filters
from .serializer import CategorySerializer,ProductSerializer,OrderSerializer
from .models import Category,Product
from django.core.paginator import Paginator


class ProductManagement:

    @api_view(['GET'])
    def product_management(request):
        ser = CategorySerializer(Category.objects.all(),many=True)
        print(f"response data: {ser.data}")
        return Response(ser.data,status=status.HTTP_200_OK)
    

    @api_view(['POST'])
    def create_category(request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def create_product(request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    @api_view(['POST'])
    def create_order(request):
        product_id = request.data.get("product")
        qty = int(request.data.get("qty", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Invalid Product ID"}, status=400)

        total = float(product.price) * qty

        # Attach total to request data
        order_data = {
            "product": product.id,
            "qty": qty,
            "total": total
        }

        serializer = OrderSerializer(data=order_data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Order created", "data": serializer.data},
                status=201
            )
        return Response(serializer.errors, status=400)


    @api_view(['GET'])
    def list_products(request):
        queryset = Product.objects.all()

        # ---------- FILTERS ----------
        category_id = request.GET.get("category")
        min_price = request.GET.get("min_price")     # ?min_price=100
        max_price = request.GET.get("max_price")     # ?max_price=500
        stock = request.GET.get("stock")             # ?stock=10

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if stock:
            queryset = queryset.filter(stock__gte=stock)

        # ---------- SEARCH ----------
        search = request.GET.get("search")  # ?search=lap
        if search:
            queryset = queryset.filter(name__icontains=search)

        # ---------- PAGINATION ----------
        page_number = request.GET.get("page", 1)
        page_size = request.GET.get("page_size", 10)

        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page_number)

        serializer = ProductSerializer(page_obj, many=True)

        return Response({
            "total": paginator.count,
            "pages": paginator.num_pages,
            "current_page": page_obj.number,
            "results": serializer.data
        })

