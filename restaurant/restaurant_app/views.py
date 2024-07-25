from django.shortcuts import render

def index(request):
    return render(request, "restaurant_app/index.html")

def order_list(request):
    return render(request, "restaurant_app/order_list.html")

def create_order(request):
    return render(request, "restaurant_app/create_order.html")

def order_detail(request, pk):
    return render(request, "restaurant_app/order_detail.html", {"order_id": pk})

def update_order(request, pk):
    return render(request, "restaurant_app/update_order.html", {"order_id": pk})

def product_list(request):
    return render(request, "restaurant_app/product_list.html")

def create_product(request):
    return render(request, "restaurant_app/create_product.html")