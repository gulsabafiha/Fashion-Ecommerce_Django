from django.contrib import admin

from .models import *

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city']


class ProductImageAdmin(admin.StackedInline):
    model = Productimage


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'rating', 'price', 'offer_price', 'introduction', 'color', 'small',
                    'medium', 'large', 'short_description', 'brand', 'short_additonal_information', 'hover_image',
                    'short_shipping_information', 'is_featured', 'side_img1', 'side_img2', 'side_img3','side_img4']
    # inlines=[ProductImageAdmin]


@admin.register(Brand)
class BrandModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand']


@admin.register(Size)
class SizeModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'size']


@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display = ['tag']


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['category']


@admin.register(Cupon)
class CuponModelAdmin(admin.ModelAdmin):
    list_display = ['cupon']


@admin.register(Review)
class ReviewModelAdmin(admin.ModelAdmin):
    list_display = ['review']


@admin.register(Questions)
class QuestionsModelAdmin(admin.ModelAdmin):
    list_display = ['questions']


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity']


@admin.register(Billing_details)
class BillingDetailModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'street_address', 'apartments',
                    'town_City', 'state_Country', 'postcode_zip', 'phone', 'email']


@admin.register(OrderPlaced)
class OrderPlacedAdminModel(admin.ModelAdmin):
    list_display=['id','user','cart','ordered_date']


@admin.register(PaymentGatewaySettings)
class PaymentGatewaySettingsAdminModel(admin.ModelAdmin):
    liset_display=['store_id','store_pass']