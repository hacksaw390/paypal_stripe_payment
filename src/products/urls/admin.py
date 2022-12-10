from django.urls import path


from products.views.admin import (
   ProductCategoryListCreateAPIView,
   ProductCategoryRetrieveUpdateAPIView,
   ProductSubCategoryListCreateAPIView,
   ProductSubCategoryRetrieveUpdateAPIView,
   ProductBrandListCreateAPIView,
   ProductBrandRetrieveUpdateAPIView,
   ProductListCreateAPIView,
   ProductRetrieveUpdateAPIView,
   ProductReviewListCreateAPIView,
   ProductReviewRetrieveUpdateAPIView,
   ProductStockListAPIView,
   ProductStockRetrieveUpdateAPIView
)

app_name = 'admin'

urlpatterns = [
    path('product-category/', ProductCategoryListCreateAPIView.as_view(), name="product_category_list_create"),
    path('product-category/<int:pk>/', ProductCategoryRetrieveUpdateAPIView.as_view(), name="product_category_retrieve_update"),
    path('product-sub-category/', ProductSubCategoryListCreateAPIView.as_view(), name="product_sub_category_list_create"),
    path('product-sub-category/<int:pk>/', ProductSubCategoryRetrieveUpdateAPIView.as_view(), name="product_sub_category_retrieve_update"),
    path('product-brand/', ProductBrandListCreateAPIView.as_view(), name="product_brand_list_create"),
    path('product-brand/<int:pk>/', ProductBrandRetrieveUpdateAPIView.as_view(), name="product_brand_retrieve_update"),

    path('product/', ProductListCreateAPIView.as_view(), name="product_list_create"),
    path('product/<int:pk>/', ProductRetrieveUpdateAPIView.as_view(), name="product_retrieve_update"),
    path('product-review/', ProductReviewListCreateAPIView.as_view(), name="product_review_list_create"),
    path('product-review/<int:pk>/', ProductReviewRetrieveUpdateAPIView.as_view(), name="product_review_retrieve_update"),
    
    path('product-stock-list/', ProductStockListAPIView.as_view(), name="product_stock_list_create"),
    path('product-stock/<int:pk>/', ProductStockRetrieveUpdateAPIView.as_view(), name="product_stock_retrieve_update")
    
]
