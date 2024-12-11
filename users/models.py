from email.policy import default

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


# Create your models here.
USER_CHOICES = (
    ('1', 'OWNER'),
    ('2', 'CHEMIST'),
)

class CustomUser(AbstractUser):
    user_type = models.CharField(choices=USER_CHOICES, max_length=50, default='1')
    profile_pic = models.ImageField(upload_to='media/profile_pic', blank=True, null=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

class Doctor(models.Model):
    doc_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    manufacturer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    country=models.CharField(max_length=50,default='unknown')
    city=models.CharField(max_length=50,default='unknown')
    state=models.CharField(max_length=50,default='unknown')

    def __str__(self):
        return self.name

class Medicine(models.Model):
    med_id = models.CharField(max_length=50, primary_key=True)  # Manually set med_id
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)  # Field for generic name
    weight = models.CharField(max_length=50)  # Changed to CharField
    category = models.CharField(max_length=100)  # Field for category
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)  # Field for manufacturer
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expire_date = models.DateField()  # Field for expiration date

    def __str__(self):
        return self.name


class Inventory(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)  # Link to Medicine
    quantity = models.PositiveIntegerField()  # Quantity in stock
    added_date = models.DateTimeField(default=timezone.now)# Date when the medicine was added to inventory
    expire_date = models.DateField()
    updated_date = models.DateTimeField(auto_now=True)  # Date when the inventory record was last updated

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity} in stock"

    class Meta:
        unique_together = ('medicine',)  # Ensure each medicine is unique in the inventory

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    cust_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone_no = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True)
    gender = models.CharField(max_length=50, blank=True)
    doc_id = models.ForeignKey(Doctor, on_delete=models.CASCADE,default=1)
    age = models.PositiveIntegerField()
    status = models.CharField(max_length=10)  # Changed to CharField

    def __str__(self):
        return self.name

class Prescription(models.Model):
    pres_id = models.AutoField(primary_key=True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doc_id = models.ForeignKey('Doctor', on_delete=models.CASCADE, null=True, blank=True,default=1)

    def __str__(self):
        return f"Prescription PR{self.pres_id} for {self.cust_id.name}"

class Bill(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment_mode=models.CharField(max_length=50,default='CASH')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill {self.id} for {self.customer.name}"

class MedDetails(models.Model):
    med_detail_id = models.AutoField(primary_key=True)
    pres_id = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='med_details')
    med_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Detail for {self.pres_id} - {self.med_id.name} ({self.quantity})"

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    med_id = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_amount=models.DecimalField(max_digits=10, decimal_places=2,default=0)
    placed_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order {self.order_id} for {self.manufacturer.name}"

class Expenses(models.Model):
    exp_id = models.AutoField(primary_key=True)
    expense_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    expense_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Expense {self.expense_type} for {self.expense_amount}"


class Incomes(models.Model):
    income_id = models.AutoField(primary_key=True)
    description = models.TextField(blank=True)
    income_type = models.CharField(max_length=50)
    income_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Income {self.income_type} for {self.income_amount}"


