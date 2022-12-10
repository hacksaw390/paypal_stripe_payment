from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from base.type_choices import PaymentStatusOptions, PaymentTypeOptions
# Create your models here.

class Payment(models.Model):
    order = models.ForeignKey("orders.Order", related_name="order_payment", on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_type = models.CharField(max_length=30, choices=PaymentTypeOptions.choices)
    payment_status = models.CharField(max_length=30, choices=PaymentStatusOptions.choices)
    transaction_number = models.CharField(max_length=150, null=True, blank=True)
    amount = models.FloatField()

    def __str__(self):
        return self.order.invoice_no
    