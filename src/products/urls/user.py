from django.urls import path

from products.views.user import (
    ProductListAPIView,
    ProductRetrieveAPIView,
    ProductCategoryListAPIView,
    UserProductReviewListCreateAPIView,
    PopularProductListAPIView,
    OrderProductListAPIView
)

app_name = 'user'

urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name="product_list"),
    path('product-category/', ProductCategoryListAPIView.as_view(), name="product_category_list"),
    path('product/<int:pk>/', ProductRetrieveAPIView.as_view(), name="product_retrieve"),
    path('product-reviews/', UserProductReviewListCreateAPIView.as_view(), name="product_review_list_create"),
    path('popular-products/', PopularProductListAPIView.as_view(), name="popular_product_list"),
    path('order-products/', OrderProductListAPIView.as_view(), name="order_list"),

]
