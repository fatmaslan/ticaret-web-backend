from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ProductVariantViewSet, ProductImageViewSet, CategoryViewSet,ProductDetaiLViewSet,AddToCartView,CartDetailView,AllCartsView,ProductListByCategory,BrandList,SliderViewSet,SliderImageViewSet
from .views import RegisterView, LoginView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'variants', ProductVariantViewSet)
router.register(r'images', ProductImageViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'sliders',SliderViewSet)
router.register(r'sliderImages',SliderImageViewSet)
router.register(r'products', ProductDetaiLViewSet, basename="product-detail")





urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('cart/', CartDetailView.as_view(), name='cart-detail'),
    path('carts/', AllCartsView.as_view(), name='all-carts'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/<int:cart_item_id>/remove/', views.remove_cart_item, name='remove_cart_item'),
    path('products/category/<str:category_name>/', ProductListByCategory.as_view(), name='products-by-category'),
    path("brands/", BrandList.as_view(), name="brand-list"),
    
]


urlpatterns += router.urls
