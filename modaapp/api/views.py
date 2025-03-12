from rest_framework import viewsets
from modaapp.models import Product, ProductVariant,ProductImages,Category,CustomUser,Cart,CartItem,SliderImages,Slider
from .serializers import ProductSerializer, ProductVariantSerializer,ProductImageSerializer,CategorySerializer,RegisterSerializer,CartItemSerializer,CartSerializer,SliderImageSerializer,SliderSeralizer
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import action
from rest_framework import status, views
CustomUser = get_user_model()
from rest_framework.decorators import api_view
from rest_framework import generics



class ProductViewSet(viewsets.ModelViewSet):
   queryset = Product.objects.all()
   serializer_class = ProductSerializer
   def get(self, request, *args, **kwargs):
        product_id = kwargs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
            variants = ProductVariant.objects.filter(product=product)
            data = {
                "id": product.id,
                "title": product.title,
                "price": str(product.price),
                "description": product.description,
                "variants": [variant.id for variant in variants]  # Variantları gönder
            }
            return Response(data)
        except Product.DoesNotExist:
            return Response({"error": "Ürün bulunamadi"}, status=status.HTTP_404_NOT_FOUND)


class ProductDetaiLViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class ProductVariantViewSet(viewsets.ModelViewSet):
   queryset = ProductVariant.objects.all()
   serializer_class = ProductVariantSerializer
   

class ProductImageViewSet(viewsets.ModelViewSet):
   queryset= ProductImages.objects.all()
   serializer_class = ProductImageSerializer
   parser_classes=[MultiPartParser,FormParser]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class RegisterView(APIView):
   serializer_class=RegisterSerializer
   permission_classes = [permissions.AllowAny]

   def post(self,request):
      username = request.data.get("username")
      email = request.data.get("email")
      password = request.data.get("password")

      if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Kullanici adi zaten mevcut"}, status=status.HTTP_400_BAD_REQUEST)
      
      if CustomUser.objects.filter(email=email).exists():
            return Response({"error": "E-posta zaten mevcut"}, status=status.HTTP_400_BAD_REQUEST)
      
      user = CustomUser.objects.create_user(username=username, email=email, password=password)    
      return Response({"message": "Kullanici başariyla oluşturuldu"}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        
        username = request.data.get("username")
        password = request.data.get("password")


        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({"error": "Geçersiz kullanici adi veya şifre"}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
        })
    



class CartDetailView(APIView):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"detail": "Sepetiniz boş."}, status=404)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        if not user or not user.is_authenticated:
            return Response({"error": "Authentication required."}, status=status.HTTP_401_UNAUTHORIZED)

        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity", 1)
        variant_id = request.data.get("variant_id")

        if not product_id or not variant_id:
            return Response({"error": "Product ID ve Variant ID gereklidir."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
            variant = ProductVariant.objects.get(id=variant_id, product=product)
        except Product.DoesNotExist:
            return Response({"error": "Ürün bulunamadi."}, status=status.HTTP_404_NOT_FOUND)
        except ProductVariant.DoesNotExist:
            return Response({"error": "Ürün varyanti bulunamadi."}, status=status.HTTP_404_NOT_FOUND)

        if variant.stock < quantity:
            return Response({"error": f"Yetersiz stok! Sadece {variant.stock} adet mevcut."}, status=status.HTTP_400_BAD_REQUEST)

        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            variant=variant,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)


class AllCartsView(APIView):
    queryset = CartItem.objects.select_related('product').all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({"detail": "Sepetiniz boş."}, status=404)
        
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
@api_view(['DELETE'])
def remove_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(id=cart_item_id)

        # Silme işlemi
        cart_item.delete()

        return Response({"message": "Ürün sepetten silindi."}, status=status.HTTP_204_NO_CONTENT)
    except CartItem.DoesNotExist:
        return Response({"error": "Sepette böyle bir ürün yok."}, status=status.HTTP_404_NOT_FOUND)



class ProductListByCategory(generics.ListAPIView):
    serializer_class=ProductSerializer

    def get_queryset(self):
        category_name=self.kwargs.get("category_name")

        if category_name == "all":
            return Product.objects.all()
        elif category_name.lower() == "brands":
            return Product.objects.exclude(brand__isnull=True).exclude(brand="")
        else:
           category = Category.objects.filter(name=category_name).first()
           if category:
                return Product.objects.filter(categories=category)
           else:
                return Product.objects.none()
        
class BrandList(APIView):
    def get(self,request):
        brands = Product.objects.values_list("brand", flat=True).distinct().exclude(brand__isnull=True).exclude(brand="")
        return Response({"brands": list(brands)})
    

class SliderViewSet(viewsets.ModelViewSet):
   queryset= Slider.objects.all()
   serializer_class = SliderSeralizer
   parser_classes=[MultiPartParser,FormParser]

class SliderImageViewSet(viewsets.ModelViewSet):
   queryset= SliderImages.objects.all()
   serializer_class = SliderImageSerializer
   parser_classes=[MultiPartParser,FormParser]