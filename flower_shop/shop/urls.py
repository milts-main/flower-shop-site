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
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('orders/', views.orders_history, name='orders_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
    path('update_cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('order/<int:order_id>/status/', views.update_order_status, name='update_order_status'),
]