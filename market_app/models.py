from django.db import models

# Create your models here.

class Market(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    net_worth = models.DecimalField(max_digits=100, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Seller(models.Model):
    name = models.CharField(max_length=255)
    markets = models.ManyToManyField(Market, related_name='sellers')
    contact_info = models.TextField()

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=50, decimal_places=2)
    description = models.TextField()
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name='products')
    market = models.ForeignKey(Market, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"Produkt: {self.name} - Preis: {self.price}€"