from django.utils.decorators import method_decorator
from base.helpers.decorators import exception_handler
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from orders.models import Order, PromoCode
from orders.serializers import OrderSerializer, PromoSerializer
from rest_framework.permissions import IsAuthenticated
from base.permissions import IsStaff, IsSuperUser
from base.permissions import HasRequiredPermissionForMethod
from orders.filters import AdminOrderFilter
from base.helpers.utils import entries_to_remove

class AdminOrderListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['orders.view_order']
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    search_fields = ['invoice_no', 'customer__email']
    filterset_class = AdminOrderFilter
    

class AdminOrderRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['orders.view_order']
    patch_permission_required = ['products.change_order']
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    http_method_names = ['patch', 'get']
    removable_keys = ('invoice_no','customer', 'total_price','discount_amount','net_price','paid_amount','due_amount','shipping_address','billing_address')
    
    def get_queryset(self):
        return super().get_queryset().filter(customer=self.request.user)

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        request.data['updated_by'] = request.user.id
        self.request.data.update(entries_to_remove(self.request.data, self.removable_keys))
        return super(AdminOrderRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)
    

class PromoCodeListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['orders.view_promocode']
    post_permission_required = ['orders.add_promocode']
    serializer_class = PromoSerializer
    queryset = PromoCode.objects.all()
    search_fields = ['code']

    

class PromoCodeRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['orders.view_promocode']
    patch_permission_required = ['orders.change_promocode']
    serializer_class = PromoSerializer
    queryset = PromoCode.objects.all()
    http_method_names = ['patch', 'get']