import uuid
from django.db import models
from django.contrib.auth.models import User

class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # Can be replaced with a ForeignKey to your custom user model if required
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Drug(models.Model):
    STOCK_STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('sold', 'Sold'),
        ('out_of_stock', 'Out of Stock'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image_url = models.URLField(max_length=500)  # To store the image path or URL
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='drugs')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='drugs', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    stock_status = models.CharField(
        max_length=15,
        choices=STOCK_STATUS_CHOICES,
        default='in_stock',
    )  # New field to track stock status

    def __str__(self):
        return self.name


class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='orders')
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    expected_delivery_date = models.DateTimeField()
    status = models.CharField(max_length=50, default='pending')  # e.g., 'pending', 'shipped', 'delivered'

    def __str__(self):
        return f"Order {self.id} - {self.status}"




class Prescription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='prescriptions')
    prescribed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions')
    dosage = models.CharField(max_length=255)  # e.g., "Take 1 tablet twice a day"
    prescribed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Prescription for {self.prescribed_to.username}"



class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=50)  # e.g., 'added', 'updated', 'deleted'
    quantity_changed = models.IntegerField()  # Can be positive or negative
    performed_by = models.CharField(max_length=255)  # Can link to a User or Staff model
    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.drug.name} by {self.performed_by}"


class Sale(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='sales')
    quantity = models.PositiveIntegerField()
    sold_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale of {self.drug.name} on {self.sold_at}"


class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name


class Discount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='discounts')
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return f"{self.percentage}% off on {self.drug.name}"


class StockAlert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name='stock_alerts')
    threshold = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.drug.name} below {self.threshold} units"

