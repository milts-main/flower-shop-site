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
    ('processing', 'В обработке'),
    ('delivered', 'Доставлен'),
    ('cancelled', 'Отменён'),
    ]
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='cart')

    def __str__(self):
        return f"Order {self.id} ({self.user.username})"

    # Итоговая стоимость всего заказа
    @property
    def total_cost(self):
        return sum(item.total_price for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.flower.name}"

    # Цена за одну единицу — берем price из OrderItem или цену цветка
    @property
    def unit_price(self):
        return self.price if self.price else self.flower.price

    # Итоговая цена этого OrderItem
    @property
    def total_price(self):
        return self.unit_price * self.quantity