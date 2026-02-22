from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='shop/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='catalog'), name='logout'),
    path('add/', views.add_flower, name='add_flower'),
]