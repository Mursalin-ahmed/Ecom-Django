from lib2to3.fixes.fix_input import context
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.shortcuts import render, redirect
from sslcommerz_lib import SSLCOMMERZ


from .models import Category, Product, cart


# Create your views here.

def shop_page(request,id):
    prod = Product.objects.get(id=id)
    return render(request, "shop.html", locals())

def cat_shop(request, id):
    cat = Category.objects.get(id=id)
    prod = Product.objects.filter(cate = cat)
    return render(request,"cat_shop.html",locals())

def addtocart(request,id):
    user = request.user
    prod = Product.objects.get(id=id)
    if user.is_authenticated:
        try:
            # Get the cart item for the specified user and product
            cartItem = cart.objects.get(Q(prod=prod) & Q(user=user))
            # If it exists, increment the quantity
            cartItem.quantity += 1
            cartItem.save()
        except cart.DoesNotExist:
            # If it doesn't exist, create a new cart item with quantity set to 1
            cartItem = cart.objects.create(user=user, prod=prod, quantity=1)

    return redirect(request.META['HTTP_REFERER'])

def product_list(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'product_list.html', context)

def remove_cart(request,id):
    prod = Product.objects.get(id = id)
    cart_item = cart.objects.get(user=request.user,prod=prod)
    cart_item.delete()
    return redirect(request.META['HTTP_REFERER'])

def decrement_cart(request,id):
    prod = Product.objects.get(id=id)
    cart_item = cart.objects.get(user=request.user, prod=prod)
    if cart_item == 1:
        cart_item.delete()
    else:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect(request.META['HTTP_REFERER'])

def increment_cart(request,id):
    prod = Product.objects.get(id=id)
    cart_item = cart.objects.get(user=request.user, prod=prod)
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(request.META['HTTP_REFERER'])

def cart_page(request,id):
    user = request.user
    cart_items = cart.objects.filter(user = user)
    total_cart = len(cart_items)

    subtotal = 0

    for i in cart_items:
        total = i.prod.price * i.quantity
        subtotal += total
    total = subtotal + 10
    return render(request, "checkout.html", locals())



def transaction_success(request, id):
    prod = Product.objects.get(id=id)
    return render(request, "transaction_success.html", )

def payment_cancel(request):
    return render(request, "payment_cancel.html")
def payment_fail(request):
    return render(request, "payment_fail.html")




def payment_getway(request,id):
    prod = Product.objects.get(id=id)
    user = request.user
    cart_items = cart.objects.filter(user=user)
    total_cart = len(cart_items)

    subtotal = 0

    for i in cart_items:
        total = i.prod.price * i.quantity
        subtotal += total
    total = subtotal + 10

    success_url = reverse('transaction_success', args=[prod.id])
    print("Success URL:", success_url)

    settings = {'store_id': 'mursa672ca9fa9bf0f', 'store_pass': 'mursa672ca9fa9bf0f@ssl', 'issandbox': True}
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = total
    post_body['currency'] = "BDT"
    post_body['tran_id'] = "12345"
    post_body['success_url'] = success_url
    post_body['fail_url'] = reverse('payment_fail')
    post_body['cancel_url'] = reverse('payment_cancel')
    post_body['emi_option'] = 0
    post_body['cus_name'] = user.username
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = "01700000000"
    post_body['cus_add1'] = "customer address"
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Test"
    post_body['product_category'] = "Test Category"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body)  # API response

    gateway_url = response['GatewayPageURL']
    gateway_url_with_params = f"{gateway_url}?product_id={prod.id}&user={request.user.username}"

    return HttpResponseRedirect(gateway_url_with_params)
