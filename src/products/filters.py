import django_filters
from products.models import Product, ProductReview, ProductSubCategory


class AdminProductSubCategoryFilter(django_filters.FilterSet):
    class Meta:
        model = ProductSubCategory
        fields = ('category',)

class UserProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ('category',)

class AdminProductReviewFilter(django_filters.FilterSet):
    class Meta:
        model = ProductReview
        fields = ('product',)