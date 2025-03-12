from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    username = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255,blank=True, null=True)
    passwordConfirm = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return self.email


class Category(models.Model):
    name=models.CharField(max_length=200,blank=True, null=True)


    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    categories=models.ManyToManyField(Category,related_name='categories',blank=True)
    brand=models.CharField(max_length=255,blank=True,null=True)


    def __str__(self):
        return self.title

class ProductImages(models.Model):
    product=models.ForeignKey(Product,related_name='images',on_delete=models.CASCADE)
    image=models.ImageField(upload_to="food_images/")

    def __str__(self):
         return f"Image of {self.product.title}"
    

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=10)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0) #Stok

    def __str__(self):
        return f"{self.product.title} - {self.color} - {self.size}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")  # Eklendi!
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,null=True, blank=True)  
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE) 
    quantity = models.PositiveIntegerField(default=1)
   

    def __str__(self):
        return f"{self.variant.product.title} - {self.variant.color} - {self.variant.size} x {self.quantity}"




class Slider(models.Model):
    title=models.CharField(max_length=255,blank=True,null=True)

    def __str__(self):
        return self.title

class SliderImages(models.Model):
    slider=models.ForeignKey(Slider,related_name='sliderimages',on_delete=models.CASCADE,blank=True,null=True)
    image=models.ImageField(upload_to="slider_images/")
   



