from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

    def __str__(self):
        return f"my name is: {self.username}  my id is: {self.id}"


class Car(models.Model):

    current_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owned_cars')
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"my brand is: {self.make} my model is: {self.model}"


class Contract(models.Model):
    PURCHASE = 'purchase'
    SALE = 'sale'

    CONTRACT_TYPE_CHOICES = [
        (PURCHASE, 'Purchase'),
        (SALE, 'Sale'),
    ]

    contract_type = models.CharField(max_length=10, choices=CONTRACT_TYPE_CHOICES, default=PURCHASE)
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales')
    total_price = models.DecimalField(max_digits=12,  decimal_places=2, null=True, blank=True)
    cars = models.ManyToManyField(Car, through='ContractCar', related_name='contracts')
    contract_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Contract #{self.id} - {self.get_contract_type_display()} ({self.contract_date})"


class ContractCar(models.Model):

    individual_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = [['contract', 'car']]

    def __str__(self):
        return f"{self.car} in {self.contract}"



