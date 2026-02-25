from .models import Flower, Order, OrderItem
from .forms import RegisterForm, CheckoutForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.


class UserLoginView(LoginView):
    template_name = 'shop/login.html'

def catalog(request):
    flowers = Flower.objects.all()

    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='cart').first()
        cart_count = order.items.count() if order else 0
    else:
        cart_count = 0

    return render(request, 'shop/catalog.html', {
        'flowers': flowers,
        'cart_count': cart_count
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        order.status = new_status
        order.save()

    return redirect('orders_history')

@login_required
@staff_member_required
def add_flower(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')

        Flower.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image
        )

        return redirect('catalog')

    return render(request, 'shop/add_flower.html')

@login_required(login_url='register')  # неавторизованный → регистрация
def add_to_cart(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)

    order, created = Order.objects.get_or_create(
        user=request.user,
        status='cart'
    )

    item, created = OrderItem.objects.get_or_create(
    order=order,
    flower=flower,
    defaults={'price': flower.price}
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect('cart')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # сразу авторизуем пользователя
            return redirect('catalog')  # после регистрации идём в каталог
    else:
        form = UserCreationForm()
    
    return render(request, 'shop/register.html', {'form': form})

@login_required(login_url='register')
def cart(request):
    if request.user.is_authenticated:
        order = Order.objects.filter(user=request.user, status='cart').first()
        items = order.items.all() if order else []
    else:
        items = []

    total = sum(item.total_price for item in items)  # итог по корзине

    return render(request, 'shop/cart.html', {
        'items': items,
        'total': total
    })

@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, status='cart').first()

    if not order:
        return redirect('cart')

    if request.method == 'POST':
        order.address = request.POST.get('address')
        order.phone = request.POST.get('phone')
        order.comment = request.POST.get('comment')

        order.status = 'placed'   # 👈 у тебя такой статус в модели!
        order.save()

        return redirect('orders_history')

    return render(request, 'shop/checkout.html', {
        'order': order,
        'items': order.items.all()
    })

# @login_required
# def remove_from_cart(request, item_id):
#     item = get_object_or_404(OrderItem, id=item_id)
    
#     if item.order.user == request.user:
#         item.delete()
    
#     return redirect('cart')

@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)

    if item.order.user == request.user:
        item.quantity += 1
        item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id)

    if item.order.user == request.user:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()

    return redirect('cart')

@login_required
def orders_history(request):

    # Если менеджер — показываем ВСЕ заказы
    if request.user.is_staff:
        orders = Order.objects.exclude(status='cart').order_by('-date')

    # Если обычный пользователь — только его
    else:
        orders = Order.objects.filter(
            user=request.user
        ).exclude(status='cart').order_by('-date')

    return render(request, 'shop/orders_history.html', {
        'orders': orders,
        'Order': Order
    })
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    cart_count = order.items.count() if order else 0
    return render(request, 'order_detail.html', {'order': order})

@login_required
def update_cart(request, item_id):
    item = OrderItem.objects.get(id=item_id, order__user=request.user, order__status='cart')
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            item.quantity += 1
        elif action == 'decrease' and item.quantity > 1:
            item.quantity -= 1
        item.save()
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    item = OrderItem.objects.get(id=item_id, order__user=request.user, order__status='cart')
    if request.method == 'POST':
        item.delete()
    return redirect('cart')

