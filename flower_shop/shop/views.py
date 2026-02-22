from django.shortcuts import render
from .models import Flower, Order, OrderItem
from .forms import RegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404

# Create your views here.

def catalog(request):
    flowers = Flower.objects.all()
    return render(request, 'shop/catalog.html', {'flowers': flowers})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            group = Group.objects.get(name='Customer')
            user.groups.add(group)

            return redirect('catalog')
    else:
        form = RegisterForm()
    
    return render(request, 'shop/register.html', {'form': form})

@login_required
@permission_required('shop.add_flower', raise_exception=True)
def add_flower(request):
    return render(request, 'shop/add_flower.html')

@login_required
def add_to_cart(request, flower_id):
    flower = get_object_or_404(Flower, id=flower_id)
    order, created = Order.objects.get_or_create(user=request.user, status='cart')
    order_item, created_item = OrderItem.objects.get_or_create(order=order, flower=flower)
    if not created_item:
        order_item.quantity += 1
        order_item.save()
    return redirect('cart')

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, status='cart').first()
    items = order.items.all() if order else []
    total = order.total_price() if order else 0
    return render(request, 'shop/cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, status='cart').first()
    if order:
        order.status = 'placed'
        order.save()
    return redirect('catalog')