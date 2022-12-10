from django.utils.decorators import method_decorator
from base.helpers.decorators import exception_handler
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from products.models import ProductCategory, Product, ProductReview
from products.serializers import ProductCategorySerializer, ProductSerializer, ProductReviewSerializer
from products.filters import UserProductFilter, AdminProductReviewFilter
from orders.models import OrderItem

class ProductCategoryListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.filter(is_active = True, show_in_ecommerce = True)

class ProductListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active = True, show_in_ecommerce = True)
    filterset_class = UserProductFilter


class ProductRetrieveAPIView(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active = True, show_in_ecommerce = True)


class UserProductReviewListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductReviewSerializer
    queryset = ProductReview.objects.all()
    filterset_class = AdminProductReviewFilter

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        product = Product.objects.get(id=request.data.get('product'))
        rating = request.data.get('rating')
        product.rating = ((product.rating * product.review_count) + rating)/(product.review_count+1)
        product.review_count = product.review_count + 1
        product.save()
        return super(UserProductReviewListCreateAPIView, self).create(request, *args, **kwargs)



class PopularProductListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(is_active = True, show_in_ecommerce = True)

    def get_queryset(self):
        return super().get_queryset().all().order_by('-popular_count')[0:10]


from django.db.models import Subquery
from rest_framework.response import Response

class OrderProductListAPIView(APIView):
    permission_classes = [IsAuthenticated]    
    def get(self, request):
        user = self.request.user
        order_item = OrderItem.objects.prefetch_related('product__category','product__sub_category','product__brand').filter(order__customer = user).order_by('-id')
        product_list = []
        break_count = 0
        for i in order_item:
            if break_count < 10:
                if i.product in product_list:
                    continue
                else:
                    product_list.append(i.product)
                    break_count = break_count+1
            else:
                break
        serializer = ProductSerializer(product_list, many=True)
        response = serializer.data
        return Response(response)