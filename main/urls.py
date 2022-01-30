from django.urls import path
from main import views
from django.conf import settings
from main.views import Home
from django.conf.urls.static import static


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('all-product/', views.allproducts, name='all-product'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:pk>', views.product, name='product'),
    path('mens-collection/', views.menscollection, name='mens-collection'),
    path('womens-collection/', views.womenscollection, name='womens-collection'),
    path('cart/', views.show_cart, name='showcart'),
    path('total cart/', views.total_cart, name='total-cart'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('removecart/<int:pk>', views.remove_cart, name='removecart'),
    path('checkout/',views.checkout,name='checkout'),
    path('categorywomen/<int:pk>',views.categoryWomenDress,name='category-women-dress'),
    path('categorymen/<int:pk>',views.categorymenDress,name='category-men-dress'),
  
    # Login urls
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
