from django.shortcuts import render, HttpResponseRedirect, redirect,get_object_or_404
from .forms import SignUpForm, LoginForm, CheckOutForm
from django.contrib.auth import authenticate, login, logout
from .models import * 
from django.views import View
from django.db.models import Q
from django.http.response import JsonResponse
from .sslcommerz import sslcommerz_payment_gateway
from django.contrib import messages

from sslcommerz_lib import SSLCOMMERZ, sslcommerz
from decimal import Decimal

# Create your views here.
class Home(View):
    def get(self, request):
        featuredProduct = Product.objects.filter(is_featured=True)
        category = Category.objects.all()
        womenWear = featuredProduct.filter(category=1)
        menWear = featuredProduct.filter(category=2)
        nonFeaturedProduct = Product.objects.filter(is_featured=False)
        arrivalwomen = nonFeaturedProduct.filter(category=1)
        arrivalmen = nonFeaturedProduct.filter(category=2)

        product = Product.objects.all().order_by('id')
        search_query = request.GET.get('search')
        if search_query != '' and search_query is not None:
            product = product.filter(title__icontains=search_query)

        cart = Cart.objects.all()
        if request.user.is_authenticated:
            cart = cart.filter(user=request.user)
            return render(request, 'index.html', {
                'carts': cart,
                'womenWear': womenWear,
                'menWear': menWear,
                'arrivalwomen': arrivalwomen,
                'arrivalmen': arrivalmen,
                'product': product
            })

        return render(request, 'index.html', {
            'womenWear': womenWear,
            'menWear': menWear,
            'arrivalwomen': arrivalwomen,
            'arrivalmen': arrivalmen,

            'product': product
        })


def allproducts(request):
    product = Product.objects.all().order_by('id')
    category = Category.objects.all()
    brand = Brand.objects.all()
    size = Size.objects.all()

    search_query = request.GET.get('search')
    if search_query != '' and search_query is not None:
        product = product.filter(title__icontains=search_query)

    category_checkboxes = request.GET.getlist('category_checkbox')
    size_checkboxes = request.GET.getlist('size_checkbox')
    brand_checkboxes = request.GET.getlist('brand_checkbox')

    if category_checkboxes:
        product = product.filter(category__in=category_checkboxes)

    if size_checkboxes:
        product = product.filter(size__in=size_checkboxes)

    if brand_checkboxes:
        product = product.filter(brand__in=brand_checkboxes)

    minPrice = request.GET.get('minPrice')
    maxPrice = request.GET.get('maxPrice')
    if minPrice != '' and maxPrice != '' and minPrice is not None and maxPrice is not None:
        product = product.filter(course_price__range=[minPrice, maxPrice])
    else:
        minPrice = 0
        maxPrice = 20000

    cart = Cart.objects.all()
    if request.user.is_authenticated:
        cart = cart.filter(user=request.user)
        return render(request, 'allproduct.html', {
            'carts': cart,
            'product': product,
            'category': category,
            'brand': brand,
            'size': size,
        })

    return render(request, 'allproduct.html',
                  {'product': product,
                   'category': category,
                   'brand': brand,
                   'size': size,
                   })


def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        return render(request, 'cart.html', {'carts': cart})
    return render(request, 'cart.html')


def total_cart(request):
    total_cart = Cart.objects.filter(user=request.user).count()
    return JsonResponse(total_cart, safe=False)


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('product')
    qty = request.GET.get('qty')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product, quantity=qty).save()
    data = {
        'string': 'Item added to cart'
    }
    return JsonResponse(data)


def remove_cart(request, pk):
    product = Product.objects.get(pk=pk)
    if request.user.is_authenticated:
        c = Cart.objects.get(user=request.user, product=product)
        c.delete()
    return redirect('showcart')


def checkout(request):
    amount=request.GET.get('totalamount')
    print(amount)
    user = request.user
    product = Cart.objects.filter(user=user)
    if request.method == 'POST':
        form = CheckOutForm(request.POST)
        if form.is_valid():
            user = user
            street_address = form.cleaned_data['street_address']
            apartments = form.cleaned_data['apartments']
            town_City = form.cleaned_data['town_City']
            state_Country = form.cleaned_data['state_Country']
            postcode_zip = form.cleaned_data['postcode_zip']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            reg = Billing_details(user=user, apartments=apartments,
                                  street_address=street_address, town_City=town_City, state_Country=state_Country, postcode_zip=postcode_zip, phone=phone, email=email)
            reg.save()
            return redirect(sslcommerz_payment_gateway(request,user,amount))
       
    else:
        form = CheckOutForm()
    return render(request, 'checkout.html', {'form': form,
                                             'product': product})



class CheckoutSuccessView(View):
    model = OrderPlaced
    template_name = 'orderPlaced.html'
 
    
    def get(self, request, *args, **kwargs):
        
        return render(request, self.template_name)
        # return HttpResponse('nothing to see')

    def post(self, request, *args, **kwargs):

        data = self.request.POST

        user = get_object_or_404(User, id=data['user_id']) #value_a is a user instance
        # cart = get_object_or_404(Cart, id = data['value_b'] ) #value_b is a user cart instance
        
        try:
            transaction=OrderPlaced.objects.create(
                user=user,
                item=data['items'],
                tran_id=data['tran_id'],
                val_id=data['val_id'],
                amount=data['amount'],
                card_type=data['card_type'],
                card_no=data['card_no'],
                store_amount=data['store_amount'],
                bank_tran_id=data['bank_tran_id'],
                status=data['status'],
                tran_date=data['tran_date'],
                currency=data['currency'],
                card_issuer=data['card_issuer'],
                card_brand=data['card_brand'],
                card_issuer_country=data['card_issuer_country'],
                card_issuer_country_code=data['card_issuer_country_code'],
                verify_sign=data['verify_sign'],
                verify_sign_sha2=data['verify_sign_sha2'],
                currency_rate=data['currency_rate'],
                risk_title=data['risk_title'],
                risk_level=data['risk_level'],

            )
            product = Cart.objects.filter(user=request.user)
            for c in product:
                OrderPlaced(user=user, cart=c).save()
                c.delete()

            messages.success(request,'Payment Successfull')

        except:
            messages.success(request,'Something Went Wrong')
        return render(request, 'orderPlaced.html')

def product(request, pk):
    product = Product.objects.all()
    product_detail = product.get(pk=pk)
    cart = Cart.objects.all()
    if request.user.is_authenticated:
        cart = cart.filter(user=request.user)
        return render(request, 'product.html', {
            'product_detail': product_detail,
            'carts': cart
        })
    return render(request, 'product.html', {
        'product_detail': product_detail
    })


def about(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user)
        return render(request, 'about.html', {
            'carts': cart
        })
    return render(request, 'about.html')


def contact(request):
    cart = Cart.objects.all()
    if request.user.is_authenticated:
        cart = cart.filter(user=request.user)
        return render(request, 'contact.html', {
            'carts': cart
        })
    return render(request, 'contact.html')


def menscollection(request):
    cart = Cart.objects.all()
    category=Category.objects.all()
    if request.user.is_authenticated:
        cart = cart.filter(user=request.user)
        return render(request, 'menscollection.html', {
            'carts': cart,'category':category
        })
    return render(request, 'menscollection.html',{
        'category':category
    })


def womenscollection(request):
    cart = Cart.objects.all()
    if request.user.is_authenticated:
        cart = cart.filter(user=request.user)
        return render(request, 'womenscollection.html', {
            'carts': cart 
        })
    return render(request, 'womenscollection.html')


def categoryWomenDress(request,pk):
    product=Product.objects.all()
    category=Category.objects.all()
    womencategory=product.filter(category=1)
    dress=womencategory.filter(category= pk)
    cart = Cart.objects.all()
    if request.user.is_authenticated:
        cart = cart.filter(user=request.user)
        return render(request, 'categorywomenDress.html', {
            'carts': cart,'dress':dress
        })
    return render(request,'categorywomenDress.html',{
        'dress':dress
    })
    
def categorymenDress(request,pk):
    product=Product.objects.all()
    category=Category.objects.all()
    mencategory=product.filter(category=2)
    mendress=mencategory.filter(category=pk)
    cart = Cart.objects.all()
    if request.user.is_authenticated:
        cart = cart.filter(user=request.user)
        return render(request, 'categorymendress.html', {
            'carts': cart,'mendress':mendress
        })
    return render(request,'categorymendress.html',{
        'mendress':mendress
    })


# Login related Views
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)

                    return HttpResponseRedirect('/')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        return HttpResponseRedirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')