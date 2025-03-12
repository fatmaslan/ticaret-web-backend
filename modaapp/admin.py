from django.contrib import admin
from .models import Product, ProductVariant,ProductImages,Category,Cart,CartItem,CustomUser,SliderImages,Slider

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
     list_display = ('id', 'name')
     search_fields = ('name',)
     list_filter = ('name',)



class ProductImagesInline(admin.TabularInline):
    model=ProductImages
    extra=3


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'get_categories') 
    list_filter = ('categories',)
    inlines = [ProductImagesInline]

    def get_categories(self,obj):
       return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description="categories"
admin.site.register(Product, ProductAdmin)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'price', 'stock')

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1  # Varsayılan olarak 1 yeni CartItem satırı ekle

class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at']  # Cart listesinde gösterilecek alanlar
    list_filter = ['user', ]  # Filtreleme seçenekleri
    search_fields = ['user__username', 'user__email']  # Kullanıcı adını ve emailini arama
    inlines = [CartItemInline]  # CartItem'ları da göstermek için inline kullanabiliriz
    fields = ['user', ]  # Admin panelinde görünen alanlar


class SliderImagesInline(admin.TabularInline):
    model=SliderImages
    extra=3

class SliderAdmin(admin.ModelAdmin):
     inlines = [SliderImagesInline]



admin.site.register(Cart, CartAdmin)
admin.site.register(CustomUser)
admin.site.register(Slider,SliderAdmin)
admin.site.register(SliderImages)
admin.site.register(ProductImages)
# admin.site.register(Category)