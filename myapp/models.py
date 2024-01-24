from django.db import models
from django.utils import timezone
# Create your models here.
class User(models.Model):
    firstname = models.CharField(max_length = 100)
    lastname = models.CharField(max_length = 100)
    mobile = models.BigIntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=20)
    profile_picture = models.ImageField(default="",upload_to="profile_picture/")
    usertype = models.CharField(max_length = 30,default="Buyer")

    def __str__(self):
        return self.firstname +" "+ self.lastname
    
class Product(models.Model):
    category = (
        ("Men","Men"),
        ("Women","Women"),
        ("Child","Child")
    )
    brand = (
        ("Levis","Levis"),
        ("Gap","Gap"),
        ("Tommy","Tommy")
    )
    size = (
        ("S","S"),
        ("M","M"),
        ("L","L"),
        ("XL","XL")
    )
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    cname = models.CharField(max_length=100, choices=category, default='Men')
    bname = models.CharField(max_length=100, choices=brand, default='Levis')
    pname = models.CharField(max_length=100)
    si = models.CharField(max_length=100, choices=size, default='M')
    desc = models.TextField()
    price = models.PositiveIntegerField()
    pimage = models.ImageField(upload_to="productimage/", default="")

    def __str__(self):
        return self.seller.firstname+" "+self.seller.lastname+"-"+self.pname

class Wishlist(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.buyer.firstname+" - "+self.product.pname

class Cart(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date=models.DateTimeField(default=timezone.now)
    product_price=models.PositiveIntegerField()
    product_qty=models.PositiveIntegerField()
    total_price=models.PositiveIntegerField()
    payment_status=models.BooleanField(default=False)

    def __str__(self):
        return self.buyer.firstname+" - "+self.product.pname