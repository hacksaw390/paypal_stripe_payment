from django.db import models
from base.models import BaseModel
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
User = get_user_model()
from base.type_choices import DiscountTypeChoices
# Create your models here.

class ProductCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    show_in_ecommerce = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_categories'

    def __str__(self):
        return self.name

class ProductSubCategory(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey("products.ProductCategory", on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    show_in_ecommerce = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_sub_categories'

    def __str__(self):
        return self.name
    
class ProductBrand(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    show_in_ecommerce = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_brands'

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=300, unique=True)
    description = models.TextField()
    category = models.ForeignKey("products.ProductCategory", on_delete=models.CASCADE)
    sub_category = models.ForeignKey("products.ProductSubCategory", on_delete=models.CASCADE)
    brand = models.ForeignKey("products.ProductBrand", on_delete=models.CASCADE)
    images = models.JSONField(default=list)
    sku = models.CharField(max_length=50)
    unit = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()
    discount_type = models.CharField(max_length=30, choices=DiscountTypeChoices.choices, default=DiscountTypeChoices.FLAT)
    discount_value = models.FloatField()
    discount_price = models.FloatField()
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    review_count = models.IntegerField(default=0)
    popular_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_in_ecommerce = models.BooleanField(default=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name


class ProductReview(BaseModel):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='product_review_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=300)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    show_in_ecommerce = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_reviews'

    def __str__(self):
        return str(self.user)