from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='shop/login.html', next_page=reverse_lazy('catalog')), name='login'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('catalog')), name='logout'),
    path('add/', views.add_flower, name='add_flower'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:flower_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
]