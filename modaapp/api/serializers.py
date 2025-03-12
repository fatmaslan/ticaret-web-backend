from rest_framework import serializers
from modaapp.models import Product, ProductVariant,ProductImages,Category,CustomUser,Cart,CartItem,SliderImages,Slider


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields='__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductVariant
        fields = ['id', 'color', 'size', 'price', 'stock']


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'description', 'variants', 'images']
        
class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True,read_only=True,source="product")
    class Meta:
        model=Category
        fields = ['id', 'name', 'products']

        
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields='__all__'

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.product and obj.product.images.exists():
            # Birincil resmi almak için ilk resmi seçebilirsiniz
            return obj.product.images.first().image.url
        return None
    

    class Meta:
        model = CartItem
        fields = ["id", "product", "image","quantity", "variant"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source="cart_items")
    class Meta:
        model=Cart
        fields = ['user', 'items']


class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SliderImages
        fields='__all__'

class SliderSeralizer(serializers.ModelSerializer):
    images= SliderImageSerializer(many=True, read_only=True)
    class Meta:
        model = Slider
        fields='__all__'