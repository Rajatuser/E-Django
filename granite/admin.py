from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *


# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('first_name', 'last_name', 'email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('first_name', 'last_name', 'email',)
    ordering = ('email',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'product_name', 'product_image', 'product_image_hover', 'product_quantity',
                    'product_actual_price', 'product_discount_price'
                    ]


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'sale', 'sale_price']



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['added_by', 'product_added']
