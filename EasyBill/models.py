from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-creation_date']


class Invoice(models.Model):
    class Status(models.TextChoices):
        PAID = 'paid', 'paid'
        UNPAID = 'unpaid', 'unpaid'
        PENDING = 'pending', 'pending'
    
    client = models.ForeignKey('Client', on_delete=models.CASCADE, related_name='invoices')
    invoice_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)
    description = models.TextField(blank=True , default="")
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))], help_text="Tax percentage (0-100)")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))], help_text="Discount percentage (0-100)")
    items = models.JSONField(default=list)  # Structure: [{"name": "Item 1", "quantity": 1, "unit_price": "10.00"}]

    class Meta:
        ordering = ['-invoice_date']
        indexes = [models.Index(fields=['-invoice_date']), models.Index(fields=['status'])]

    def __str__(self):
        return f"Invoice {self.id} for {self.client.name}"

    @property
    def calculate_total(self):
        subtotal = sum(Decimal(str(item['unit_price'])) * item['quantity'] for item in self.items)
        discount_amount = subtotal * (self.discount / Decimal('100'))
        subtotal_after_discount = subtotal - discount_amount
        tax_amount = subtotal_after_discount * (self.tax / Decimal('100'))
        return subtotal_after_discount + tax_amount

    def save(self, *args, **kwargs):
        self.total = self.calculate_total
        super().save(*args, **kwargs)