from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Flower(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='flowers/', null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('cart', 'В корзине'),
        ('placed', 'Оформлен'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')

    def __str__(self):
        return f"Order {self.id} ({self.user.username})"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    flower = models.ForeignKey('Flower', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.flower.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.flower.name}"