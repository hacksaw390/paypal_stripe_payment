from rest_framework import serializers
from base.serializers import DynamicFieldsModelSerializer
from products.models import ProductCategory, ProductSubCategory, ProductBrand, Product, ProductReview
from base.serializers import ReadWriteSerializerMethodField
from accounts.serializers import UserLiteSerializer

class ProductCategorySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'is_active', 'show_in_ecommerce','created_by','updated_by')

class ProductCategoryLiteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'is_active')

class ProductSubCategorySerializer(DynamicFieldsModelSerializer):
    category = ReadWriteSerializerMethodField()
    def get_category(self, obj):
        return ProductCategoryLiteSerializer(instance=obj.category).data
    class Meta:
        model = ProductSubCategory
        fields = ('id', 'name','category', 'is_active', 'show_in_ecommerce','created_by','updated_by')

class ProductSubCategoryLiteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ProductSubCategory
        fields = ('id', 'name','is_active')

        
class ProductBrandSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ('id', 'name','is_active', 'show_in_ecommerce','created_by','updated_by')


class ProductBrandLiteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = ProductBrand
        fields = ('id', 'name','is_active')

        
class ProductSerializer(DynamicFieldsModelSerializer):
    # review_set =  ReviewSerializer(many = True, read_only = True, source='product_review_set')
    category = ReadWriteSerializerMethodField()
    sub_category = ReadWriteSerializerMethodField()
    brand = ReadWriteSerializerMethodField()
    def get_category(self, obj):
        return ProductCategoryLiteSerializer(instance=obj.category).data
    def get_sub_category(self, obj):
        return ProductSubCategoryLiteSerializer(instance=obj.sub_category).data
    def get_brand(self, obj):
        return ProductBrandLiteSerializer(instance=obj.brand).data
    class Meta:
        model = Product
        fields = (
                'id',
                'name',
                'description',
                'category',
                'sub_category',
                'brand',
                'images',
                'sku',
                'unit',
                'price',
                'discount_type',
                'discount_value',
                'discount_price',
                'rating', 
                'is_active', 
                'show_in_ecommerce',
                'created_by',
                'updated_by'
            )


class ProductLiteSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name','description')
     
class ProductReviewSerializer(DynamicFieldsModelSerializer):
    user = ReadWriteSerializerMethodField()
    def get_user(self, obj):
        return UserLiteSerializer(instance=obj.user).data
    product = ReadWriteSerializerMethodField()
    def get_product(self, obj):
        return ProductLiteSerializer(instance=obj.product).data
    class Meta:
        model = ProductReview
        fields = '__all__'



class ProductStockSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name','quantity']