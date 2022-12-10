from django.utils.decorators import method_decorator
from base.helpers.decorators import exception_handler
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from orders.models import Order, OrderItem, PromoCode
from orders.serializers import OrderSerializer, OrderItemSaveSerializer, PromoSerializer
from base.helpers.utils import identifier_builder
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from datetime import datetime
from orders.views.service import PaymentProcess
from payments.models import Payment
from products.models import Product

class UserOrderCreateView(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    
    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        requested_data = request.data
        requested_data['created_by'] = request.user.id
        requested_data['invoice_no'] = identifier_builder(table_name='orders', prefix="ORD")
        # Promo Check
        if requested_data.get('promo_code'):
            promo_code = requested_data['promo_code']
            promo = PromoCode.objects.get(code=promo_code)
            if promo.discount_type == 'percentage':
                discount_amount = (requested_data['total_price'] * promo.discount_value) / 100
            else:
                discount_amount = promo.discount_value
            net_price = requested_data['total_price'] - discount_amount
        else:
            net_price = requested_data['total_price']
        
        requested_data['net_price'] = net_price
        requested_data['due_amount'] = net_price
        order_serializer = self.serializer_class(data = requested_data)
        order_serializer.is_valid(raise_exception=True)

        products = request.data['products']
        payment_type = request.data['payment_type']
        customer_id = request.data['customer']
        # Stock Check
        stock_out_product = []
        for i in products:
            product = Product.objects.get(id=i['product'])
            if product.quantity - i['quantity'] <=0:
                stock_out_product.append(product.name)
        if stock_out_product:
            return Response({'message': f"{stock_out_product} stock out product"}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            order = order_serializer.save()
            items = []
            for i in products:
                i.update({"order": order.id})
                i.update({"created_by": request.user.id})
                product = Product.objects.get(id=i['product'])
                i.update({"unit_price": product.discount_price})
                i.update({"total_price": (product.discount_price * i['quantity'])})
                items.append(i)
            order_item_serializer = OrderItemSaveSerializer(data=items, many=True)
            order_item_serializer.is_valid(raise_exception=True)
            items = order_item_serializer.save()
            for item in items:
                product = item.product
                product.popular_count += item.quantity
                product.quantity -= item.quantity
                product.save()
            payment = Payment.objects.create(order_id=order.id, customer_id=customer_id, payment_type=payment_type, payment_status='initiated',amount=net_price)

        process_data = PaymentProcess(order.id, net_price, payment_type,payment.id, customer_id)()    
       
        return Response({'data': self.serializer_class(order).data, "url": process_data['url']}, status=status.HTTP_201_CREATED)



class UserOrderListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)
    


class UserOrderRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)

class PromoEligibilityCheck(APIView):
    permission_classes = (IsAuthenticated, )
    @method_decorator(exception_handler)
    def get(self, request, *args, **kwargs):
        promo_code = request.query_params.get('code')
        amount = request.query_params.get('amount')
        current_date = datetime.today().date()
        promo = PromoCode.objects.filter(code = promo_code, start_date__date__lte=current_date, end_date__date__gte=current_date).first()
        
        if promo:
            if int(promo.minimum_amount) > int(amount):
                return Response({'message' : f'This code will apply if the minimum amount is {promo.minimum_amount}'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(PromoSerializer(promo).data, status=status.HTTP_200_OK)
        else:
            return Response({'message' : 'Promo not valid'}, status=status.HTTP_400_BAD_REQUEST)

    

