from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


#AbstractUser is django built-in class for User creation but we need some attributes from the django user, so we inherited this class in
# our User class
class User(AbstractUser):
    class Role(models.TextChoices):

        ADMIN = "ADMIN", "Admin"
        CUSTOMER = "CUSTOMER", "Customer"
        TAILOR = "TAILOR", "Tailor"

    #Add Custom user attributes

    base_role = Role.ADMIN
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=11)
    CNIC = models.CharField(max_length=15, default='42101-4250287-7', null=False)
    password2 = models.CharField(max_length=30, null=False)
    role = models.CharField(max_length=50, choices=Role.choices)
    profile_image = models.ImageField(upload_to='./media/profile_img/' , default='default.jpg', null=True, blank=True)
    t_physical_shop_address = models.CharField(max_length=80, null=True, blank=True)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)

    def clean(self):
        if self.role == self.Role.TAILOR:
            if not self.t_physical_shop_address:
                raise ValidationError("Tailor must have a physical shop address.")

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        self.clean()

        super().save(*args, **kwargs)


#This will filter out all the customers from the users table
class CustomerManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.CUSTOMER)


class Customer(User):
    base_role = User.Role.CUSTOMER
    # customer = CustomerManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for customers"





#This will filter out all the tailors from the users table
class TailorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TAILOR)


class Tailor(User):
    base_role = User.Role.TAILOR
    class Meta:
        proxy = True

    def welcome(self):
        return "Only for tailors!"



# Shipper
class Shipper(models.Model):
    shipper_contact = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)

    def __str__(self):
        return self.company_name


# Services
def tailor_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/tailor_<tailor_id>/<filename>
    return 'tailor_{0}/{1}'.format(instance.tailor.id, filename)


class Service(models.Model):
    tailor = models.OneToOneField(Tailor, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=255, null=False)
    service_price = models.CharField(max_length=255, null=False)
    service_type = models.CharField(max_length=255, null=False)
    service_description= models.CharField(max_length=300, null=False)
    service_image = models.ImageField(upload_to='service_img/', null=True)

    def __str__(self):
        return self.service_name


# Billing Info
class BillingInfo(models.Model):
    billing_date = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.billing_date


# Orders
class Order(models.Model):
    order_date = models.CharField(max_length=255, null=False)
    order_status = models.CharField(max_length=255)
    Delivery_date = models.CharField(max_length=255)
    Pickup_date = models.CharField(max_length=255)
    Total_orders = models.CharField(max_length=255)

    def __str__(self):
        return self.order_status


# Clothes
class Clothe(models.Model):
    order_cloth = models.CharField(max_length=255)
    cloth_type = models.CharField(max_length=255)

    def __str__(self):
        return self.order_cloth


# Extras
class Extra(models.Model):
    order_extras = models.CharField(max_length=255)
    extras_type = models.CharField(max_length=255)

    def __str__(self):
        return self.order_extras



# Pickup
class Pickup(models.Model):
    pickup_date = models.CharField(max_length=255)
    pickup_time = models.CharField(max_length=255)

    def __str__(self):
        return f"data"