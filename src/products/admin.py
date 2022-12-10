from django.contrib import admin
from products.models import ProductCategory, ProductSubCategory, ProductBrand, Product, ProductReview
# Register your models here.

admin.site.register([ProductCategory,ProductSubCategory, ProductBrand, Product, ProductReview])
