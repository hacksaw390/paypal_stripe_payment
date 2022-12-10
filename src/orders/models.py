from django.db import models
from base.models import BaseModel
from django.contrib.auth import get_user_model
User = get_user_model()
from base.type_choices import OrderStatusOptions
from base.type_choices import DiscountTypeChoices
# Create your models here.

class Order(BaseModel):
    invoice_no = models.CharField(max_length=150, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.FloatField()
    discount_amount = models.FloatField(default=0)
    net_price = models.FloatField()
    order_status = models.CharField(max_length=30, choices=OrderStatusOptions.choices, default=OrderStatusOptions.PENDING)
    paid_amount = models.FloatField(default=0)
    due_amount = models.FloatField(default=0)
    shipping_address = models.ForeignKey("accounts.UserAddress", related_name="customer_shipping_address", on_delete=models.CASCADE)
    billing_address = models.ForeignKey("accounts.UserAddress", related_name="customer_billing_address", on_delete=models.CASCADE)
    class Meta:
        db_table = 'orders'

    def __str__(self):
        return self.invoice_no
    

class OrderItem(BaseModel):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="order_items_set")
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit_price = models.FloatField()
    total_price = models.FloatField()

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return self.product.name
    

class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_value = models.FloatField()
    discount_amount = models.FloatField()
    discount_type =  models.CharField(max_length=12, choices=DiscountTypeChoices.choices)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    minimum_amount = models.FloatField()
    class Meta:
        db_table = 'promo_codes'

    def __str__(self):
        return self.code