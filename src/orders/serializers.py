from rest_framework import serializers
from base.serializers import DynamicFieldsModelSerializer
from orders.models import Order, OrderItem, PromoCode
from base.serializers import ReadWriteSerializerMethodField
from accounts.serializers import UserLiteSerializer
from products.serializers import ProductLiteSerializer
class OrderItemLiteSerializer(DynamicFieldsModelSerializer):
    product = ReadWriteSerializerMethodField()
    def get_product(self, obj):
        return ProductLiteSerializer(instance=obj.product).data
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product', 
            'quantity',
            'unit_price',
            'total_price'
        )
class OrderSerializer(DynamicFieldsModelSerializer):
    items =  OrderItemLiteSerializer(many = True, read_only = True, source='order_items_set')
    customer = ReadWriteSerializerMethodField()
    def get_customer(self, obj):
        return UserLiteSerializer(instance=obj.customer).data
    class Meta:
        model = Order
        fields = (
            'id', 
            'invoice_no', 
            'customer', 
            'total_price',
            'discount_amount',
            'net_price',
            'order_status',
            'paid_amount',
            'due_amount',
            'shipping_address',
            'billing_address',
            'created_by',
            'items'
        )


class OrderItemSaveSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id', 
            'order', 
            'product', 
            'quantity',
            'unit_price',
            'total_price',
            'created_by'
        )

    
class PromoSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = PromoCode
        fields = (
            'id', 
            'code', 
            'discount_value', 
            'discount_amount',
            'discount_type',
            'start_date',
            'end_date',
            'minimum_amount'
        )