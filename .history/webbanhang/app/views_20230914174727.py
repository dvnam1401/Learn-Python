from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

def category(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    if active_category:
        product = Product.objects.filter(category_slug)
    context = {'category': categories, 'product': product}

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains=searched)
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
    products = Product.objects.all()
    context = {'searched': searched, 'keys': keys,
               'products': products, 'cartItems': cartItems}
    return render(request, 'app/search.html', context)


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'form': form}
    return render(request, 'app/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        context
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')  # lấy từ file login.html
        password = request.POST.get('password')  # lấy từ file login.html
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'user or password not correct!')
    context = {'user_not_login': "show",
        'user_login': "hidden"}
    return render(request, 'app/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('login')


def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems,
               "user_not_login": user_not_login, "user_login": user_login}
    return render(request, 'app/home.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    context = {'items': items, 'order': order, 'cartItems': cartItems,
               "user_not_login": user_not_login, "user_login": user_login}
    return render(request, 'app/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, create = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    context = {'items': items, 'order': order, 'cartItems': cartItems,
               "user_not_login": user_not_login, "user_login": user_login}
    return render(request, 'app/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productID)
    order, create = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, create = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)
