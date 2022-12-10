from django.utils.decorators import method_decorator
from base.helpers.decorators import exception_handler
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from base.permissions import IsStaff, IsSuperUser
from products.models import ProductCategory, ProductSubCategory, ProductBrand, Product, ProductReview
from products.serializers import ProductCategorySerializer, ProductSerializer, ProductSubCategorySerializer, ProductBrandSerializer, ProductReviewSerializer, ProductStockSerializer
from base.permissions import HasRequiredPermissionForMethod
from products.filters import AdminProductReviewFilter, AdminProductSubCategoryFilter
from base.helpers.utils import entries_to_remove

class ProductCategoryListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_productcategory']
    post_permission_required = ['products.add_productcategory']
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    search_fields = ['name']

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        return super(ProductCategoryListCreateAPIView, self).create(request, *args, **kwargs)


class ProductCategoryRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_productcategory']
    patch_permission_required = ['products.change_productcategory']
    serializer_class = ProductCategorySerializer
    queryset = ProductCategory.objects.all()
    http_method_names = ['patch', 'get']

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        request.data['updated_by'] = request.user.id
        return super(ProductCategoryRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)

    
class ProductSubCategoryListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_productsubcategory']
    post_permission_required = ['products.add_productsubcategory']
    serializer_class = ProductSubCategorySerializer
    queryset = ProductSubCategory.objects.all()
    search_fields = ['name','category__name']
    filterset_class = AdminProductSubCategoryFilter

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        return super(ProductSubCategoryListCreateAPIView, self).create(request, *args, **kwargs)


class ProductSubCategoryRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_productsubcategory']
    patch_permission_required = ['products.change_productsubcategory']
    serializer_class = ProductSubCategorySerializer
    queryset = ProductSubCategory.objects.all()
    http_method_names = ['patch', 'get']

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        request.data['updated_by'] = request.user.id
        return super(ProductSubCategoryRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)

class ProductBrandListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_productbrand']
    post_permission_required = ['products.add_productbrand']
    serializer_class = ProductBrandSerializer
    queryset = ProductBrand.objects.all()
    search_fields = ['name']

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        return super(ProductBrandListCreateAPIView, self).create(request, *args, **kwargs)


class ProductBrandRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_productbrand']
    patch_permission_required = ['products.change_productbrand']
    serializer_class = ProductBrandSerializer
    queryset = ProductBrand.objects.all()
    http_method_names = ['patch', 'get']

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        request.data['updated_by'] = request.user.id
        return super(ProductBrandRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)



class ProductListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_product']
    post_permission_required = ['products.add_product']
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    search_fields = ['name','category__name', 'sub_category__name']

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.user.id
        discount_type = request.data['discount_type']
        discount_value = request.data['discount_value']
        if discount_type == 'flat':
            request.data['discount_price'] = request.data['price'] - discount_value
        else:
            request.data['discount_price'] = request.data['price'] - ((request.data['price'] * discount_value)/100)
        return super(ProductListCreateAPIView, self).create(request, *args, **kwargs)


class ProductRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_product']
    patch_permission_required = ['products.change_product']
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['patch', 'get']

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        request.data['updated_by'] = request.user.id
        product = Product.objects.get(id=self.kwargs['pk'])
        
        if request.data.get('price'):
            price = request.data['price']
        else:
            price = product.price

        if request.data.get('discount_type'):
            discount_type = request.data['discount_type']
        else:
            discount_type = product.discount_type

        if request.data.get('discount_value'):
            discount_value = request.data['discount_value']
        else:
            discount_value = product.discount_value
        
        if discount_type == 'flat':
            request.data['discount_price'] = price - discount_value
        else:
            request.data['discount_price'] = price - ((price * discount_value)/100)
        return super(ProductRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)


class ProductReviewListCreateAPIView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_productreview']
    post_permission_required = ['products.add_productreview']
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
        return super(ProductReviewListCreateAPIView, self).create(request, *args, **kwargs)
    

class ProductReviewRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_productreview']
    patch_permission_required = ['products.change_productreview']
    serializer_class = ProductReviewSerializer
    queryset = ProductReview.objects.all()
    http_method_names = ['patch', 'get']

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        request.data['updated_by'] = request.user.id
        if request.data.get('rating'):
            review_rating = self.get_object().rating
            new_rating = review_rating - request.data.get('rating')
            product = self.get_object().product
            product.rating = ((product.review_count * product.rating) - new_rating) / product.review_count
            product.save()
        return super(ProductReviewRetrieveUpdateAPIView, self).patch(request, *args, **kwargs)



# Inventory
class ProductStockListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_product']
    post_permission_required = ['products.add_product']
    serializer_class = ProductStockSerializer
    queryset = Product.objects.all()
    search_fields = ['name','category__name', 'sub_category__name']


class ProductStockRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, (IsStaff | IsSuperUser),HasRequiredPermissionForMethod)
    get_permission_required = ['products.view_product']
    patch_permission_required = ['products.change_product']
    serializer_class = ProductStockSerializer
    queryset = Product.objects.all()
    removable_keys = ('name')

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        product = Product.objects.get(pk=kwargs.get("pk"))
        request.data['quantity'] = product.quantity + request.data['quantity']
        self.request.data.update(entries_to_remove(self.request.data, self.removable_keys))
        return super().patch(request, *args, **kwargs)