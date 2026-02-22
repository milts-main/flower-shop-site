from django.shortcuts import render
from .models import Flower
from .forms import RegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required

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