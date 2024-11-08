from django.urls import path
from Product.views import *

urlpatterns = [
    path('shop_page/<int:id>/', shop_page, name='shop_page'),
    path('cat_shop/<int:id>/', cat_shop, name='cat_shop'),
    path('addtocart/<int:id>/', addtocart, name='addtocart'),
    path('cart_page/<int:id>/', cart_page, name='cart_page'),
    path('increment_cart/<int:id>/', increment_cart, name='increment_cart'),
    path('decrement_cart/<int:id>/', decrement_cart, name='decrement_cart'),
    path('remove_cart/<int:id>/', remove_cart, name='remove_cart'),
    path('payment_getway/<int:id>/', payment_getway, name='payment_getway'),
    path('transaction_success/<int:id>/', transaction_success, name='transaction_success'),
    path('payment_cancel/', payment_cancel, name='payment_cancel'),
    path('payment_fail/', payment_fail, name='payment_fail'),
    path('product_list/', product_list, name='product_list'),
]


