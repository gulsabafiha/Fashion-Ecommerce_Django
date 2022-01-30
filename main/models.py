from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars
from ckeditor.fields import RichTextField


class Customer(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)

    def __str__(self):
        return str(self.id)


class Brand(models.Model):
    brand = models.CharField(max_length=50)

    def __str__(self):
        return str(self.brand)


class Tag(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    tag = models.CharField(max_length=50)

    def __str__(self):
        return str(self.tag)

class Category(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    category = models.CharField(max_length=50)

    def __str__(self):
        return str(self.category)


class Cupon(models.Model):
    cupon = models.CharField(max_length=50)

    def __str__(self):
        return str(self.cupon)


class Review(models.Model):
    review = models.CharField(max_length=50)

    def __str__(self):
        return str(self.review)


class Questions(models.Model):
    questions = models.CharField(max_length=50)

    def __str__(self):
        return str(self.questions)


class Size(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    size=models.CharField(max_length=50)

    def __str__(self):
        return str(self.size)

class Product(models.Model):
    id = models.BigAutoField(primary_key=True, null=False)
    title = models.CharField(null=True,max_length=50)
    rating = models.FloatField(null=True)
    price = models.FloatField(null=True)
    offer_price = models.FloatField(null=True)
    introduction = models.CharField(null=True,max_length=200)
    color = models.ImageField(null=True,upload_to='product-img')
    size=models.ForeignKey(Size,default=2, null=True,on_delete=models.SET_DEFAULT)
    small=models.IntegerField(null=True)
    medium=models.IntegerField(null=True)
    large=models.IntegerField(null=True)
    category = models.ManyToManyField(Category)
    tag= models.ManyToManyField('Tag')
    brand = models.ForeignKey(Brand, null=True, on_delete=models.CASCADE)
    description = RichTextField()
    additional_information = RichTextField(null=True)
    shipping_information = RichTextField(null=True)
    hover_image=models.ImageField(null=False,blank=True,upload_to='product-img')
    side_img1=models.ImageField(null=True,blank=True,upload_to='product-img')
    side_img2=models.ImageField(null=True,blank=True,upload_to='product-img')
    side_img3=models.ImageField(null=True,blank=True,upload_to='product-img')
    side_img4=models.ImageField(null=True,blank=True,upload_to='product-img')
    is_featured=models.BooleanField(default=False)
    review=models.IntegerField(null=True)

    def get_tags(self):
        return "\n".join([p.tag for p in self.tag.all()])

    @property
    def short_description(self):
        return truncatechars(self.description, 50)
    @property
    def short_additonal_information(self):
        return truncatechars(self.additional_information, 50)
    @property
    def short_shipping_information(self):
        return truncatechars(self.shipping_information, 50)

    def __str__(self):
        return str(self.title)

class Productimage(models.Model):
    image=models.ImageField(upload_to='product-img')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)


class Cart(models.Model):
    id = models.BigAutoField(primary_key=True,null=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity= models.PositiveIntegerField(default=1)

    @property
    def tempamount(self):
        tempamount=self.quantity * self.product.price
        return tempamount

    def __str__(self):
        return str(self.id)


class  Billing_details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address=models.CharField(max_length=100)
    apartments=models.CharField(max_length=100)
    town_City=models.CharField(max_length=100)
    state_Country=models.CharField(max_length=100)
    postcode_zip=models.IntegerField()
    phone=models.IntegerField()
    email=models.EmailField()

    @property
    def tempamount(self):
        tempamount=self.quantity * self.product.price
        return tempamount

class OrderPlaced(models.Model):
    id = models.BigAutoField(primary_key=True,null=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    ordered_date=models.DateTimeField(auto_now_add=True)

    @property
    def tempamount(self):
        tempamount=self.quantity * self.product.price
        return tempamount

        
class PaymentGatewaySettings(models.Model):

    store_id = models.CharField(max_length=500, blank=True, null=True)
    store_pass = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        verbose_name = "PaymentGatewaySetting"
        verbose_name_plural = "PaymentGatewaySettings"
        db_table = "paymentgatewaysettings"