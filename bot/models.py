from importlib.abc import Traversable
from django.db import models

# Create your models here.


class BotUser(models.Model):
    tg_id = models.PositiveBigIntegerField(unique=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self) -> str:
        if self.phone is not None:
            return self.phone
        return str(self.id)
    
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Menu(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Meal(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.RESTRICT)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    image = models.ImageField(upload_to="Meals/")
    def __str__(self) -> str:
        return self.name

class OrderItem(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.RESTRICT)
    order = models.ForeignKey("Order", on_delete=models.RESTRICT)
    meal = models.ForeignKey(Meal, on_delete=models.RESTRICT)
    quantitation = models.SmallIntegerField(default=1)
    total_price = models.IntegerField()
    
    @property
    def total_price(self):
        return self.meal.price * self.quantitation

class Order(models.Model):
    user = models.ForeignKey(BotUser, on_delete=models.RESTRICT)
    total_price = models.IntegerField()
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    @property
    def total_price(self):
        orderItems = OrderItem.objects.filter(order_id=self.pk).order_by("pk")
        if orderItems is not None:
            total = 0
            for orderItem in orderItems:
                total += orderItem.total_price
            return total
        return 0