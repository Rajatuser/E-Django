import self as self
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=200, primary_key=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', ]
    objects = MyUserManager()

    def __str__(self):
        return self.email


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200, unique=True)
    product_image = models.ImageField(upload_to='images/')
    product_image_hover = models.ImageField(upload_to='hover_images/')
    product_quantity = models.IntegerField()
    product_actual_price = models.DecimalField(max_digits=20, decimal_places=2)
    product_discount_price = models.DecimalField(max_digits=20, decimal_places=2)


    def __str__(self):
        return self.product_name


class SaleProduct(models.Model):
    product = models.OneToOneField(Product, related_name="sale_product", on_delete=models.CASCADE)
    sale = models.IntegerField()
    sale_price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.product)


class Cart(models.Model):
    added_by = models.ForeignKey(CustomUser, related_name='addedBy', on_delete=models.CASCADE)
    product_added = models.ForeignKey(Product, related_name='product_added', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.product_added)

