from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'image', 'created', 'amount', 'cat_id', 'author']
    list_filter = ['created']
    inlines = [ProductImageInline]
