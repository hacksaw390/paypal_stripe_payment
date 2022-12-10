from django.db import models


class UserRoleOption(models.TextChoices):
    SUPER_ADMIN = "super_admin", "super_admin"
    USER_MANAGEMENT = "user_management", "user_management"
    PRODUCT_MANAGEMENT = "product_management","product_management"
    ORDER_MANAGEMENT = "order_management", "order_management"


class AddressTypeChoices(models.TextChoices):
    SHIPPING = "shipping", "shipping"
    BILLING = "billing", "billing"


class OrderStatusOptions(models.TextChoices):
    PENDING = "pending", "pending"
    CONFIRMED = "confirmed", "confirmed"
    DELIVERED = "delivered", "delivered"
    
class PaymentStatusOptions(models.TextChoices):
    INITIATED = 'initiated', 'initiated'
    COMPLETED = 'completed', 'completed'
    CANCELLED = 'cancelled', 'cancelled'
    REJECTED = 'rejected', 'rejected'
    FAILED = 'failed', 'failed'
    PAID = 'paid', 'paid'


class PaymentTypeOptions(models.TextChoices):
    CASH_ON_DELIVERY = "cash_on_delivery", "cash_on_delivery"
    STRIPE = "stripe", "stripe"
    PAYPAL = "paypal", "paypal"

class DiscountTypeChoices(models.TextChoices):
    FLAT = "flat", "flat"
    PERCENTAGE = "percentage", "percentage"