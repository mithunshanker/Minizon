from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Categories(models.Model):
    name=models.CharField()
    slug= models.SlugField(unique=True)

class Product(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField(max_length=5000)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=4, decimal_places=2)
    category = models.ForeignKey('Categories', on_delete=models.CASCADE)
    stock = models.IntegerField()
    is_available = models.BooleanField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    img_url = models.URLField(max_length=400)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Adress(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    full_name=models.CharField(max_length=250)
    phone_number= models.CharField()
    adress= models.CharField( max_length=500)
    pincode= models.CharField(max_length=50)

class Cart(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    created_at= models.DateTimeField( auto_now=False, auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True, auto_now_add=False)

class Order(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    total_price= models.DecimalField( max_digits=8, decimal_places=2)
    adress= models.ForeignKey(Adress, on_delete=models.CASCADE)
    order_status= models.CharField( max_length=50)
    placed_at=models.DateTimeField( auto_now=False, auto_now_add=True)

class Order_item(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField()

class Cartitem(models.Model):
    cart= models.ForeignKey(Cart, on_delete=models.CASCADE)
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity=models.IntegerField()
    subtotal=models.DecimalField(max_digits=9,decimal_places=2)

    
  