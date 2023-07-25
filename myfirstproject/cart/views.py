from datetime import date
import json
from pyexpat.errors import messages
from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from store.models import product, ProductVariant,Coupon
from cart.models import Cart,Cart_Item
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from website.models import CustomUser, AddressBook
from .forms import   AddressBookForm
from django.views.decorators.http import require_POST
from order.models import CancelOrder,Wallet






@login_required
def add_cart(request):

    print("add to cart request hit")
    try:
        # fetching data
        email = request.user.email
        product_id = request.GET.get('product_id')
        user_instence = CustomUser.objects.get(email = email)
        print(email)
        print("id", product_id)
        
        # update cart table
        cart_instence,_ = Cart.objects.get_or_create(user = user_instence)
        print("cart table updated")
        # update cartitem table
        Productvarient_instance = ProductVariant.objects.get(pk=product_id)
        print("instance fetched")
        
        new_cartitem,created = Cart_Item.objects.get_or_create(user = user_instence, carts = cart_instence, product_variant = Productvarient_instance)
        print("cart item table updated")
        
        if created:
            print("new one created")
            new_cartitem.save()
        else:
            print("already excist")

    
    except Exception as e:
        print("exception found")
        print(e)
        return JsonResponse({"status":403, "message":"bad request"})

    print("noexception return responce")
    return JsonResponse({"status":201, "message":"ok"})



def delete_from_cart(request, cart_item_id):
    if request.method == "POST":
       
        
       cart_item = Cart_Item.objects.get(pk=cart_item_id)
       cart_item.delete()
    
       return redirect('view_cart')
    
def calculate_cart_total(cart_items):
    total = 0
    for cart_item in cart_items:
        
        total += cart_item.sub_total()
        
    return total 
   

def view_cart(request):
    
    # fetching data
    print("request hit")
    cart = Cart.objects.filter(user=request.user).first()
    cart_items =Cart_Item.objects.filter(carts=cart)
    cart_total = calculate_cart_total(cart_items)
    context = {
             'cart_items' : cart_items,
    'carts' : cart,
    'cart_total': cart_total
     }
    if 'total' in request.session:
            del request.session['total']
    return render (request,"cart.html", context)
   
    
    

    
   
        
        


@login_required
def update_cart_item_quantity(request):
        cart_item_id = request.GET.get('cart_item_id')
        action = request.GET.get('action')

        # cart_item = Cartitem.objects.get(id=cart_item_id)
        try:
           cart_item = Cart_Item.objects.get(id=cart_item_id) 
        except cart_item.DoesNotExist:
            return JsonResponse({'status': 404, 'error': 'Cart item not found'})

        if action == 'increase':
            if cart_item.quantity < cart_item.product_variant.stock:
                cart_item.quantity += 1
        elif action == 'decrease':
         
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
        cart_item.save()
        if 'total' in request.session:
            del request.session['total']

        return JsonResponse({'status': 200, 'quantity': cart_item.quantity, 'subtotal': cart_item.sub_total() })

class chech_out (View):

    def get(self, request):
        print("request hit")
        cart = Cart.objects.get(user=request.user)
        cart_items = Cart_Item.objects.filter(carts = cart)
        
        # calculating cart items total sum
        sum = 0
        subtotal = 0
        for item in cart_items:
            subtotal += item.sub_total()
            if (request.session.get('total')):
                
                sum = request.session.get('total')
            else:
                sum += item.sub_total()
            
        
        address = AddressBook.objects.filter(user=request.user)
        
        context = {
            'cart_items': cart_items,
            'address': address,
            'sum':sum,
            'subtotal':subtotal
        }
        print("view end")
        return render(request, 'checkout.html', context)
    
 


# def add_address(request):
#     if request.method == "POST":
#         address_form = AddressBookForm(request.POST, request.FILES)
#         if address_form.is_valid():
#             address = address_form.save(commit=False)  
#             address.user = request.user 
#             address.save() 
#             return redirect("chech_out")  
#     else:
#         address_form = AddressBookForm()
  
#     context = {'address_form': address_form}
#     return render(request, 'add_address.html', context)

def add_address(request):
    address_form = AddressBookForm()

    if request.method == "POST":
        address_form = AddressBookForm(request.POST, request.FILES)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()

            address_id = address.id  # Use the address ID from the saved object
            return redirect("payment_product", id=address_id)

    context = {'address_form': address_form}
    return render(request, 'add_address.html', context)

#edit address

def edit_address(request, address_id):
    address = get_object_or_404(AddressBook, id=address_id)

    if request.method == "POST":
        address_form = AddressBookForm(request.POST, instance=address)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect("chech_out")
    else:
        address_form = AddressBookForm(instance=address)

    context = {'address_form': address_form}
    return render(request, 'edit_address.html', context)

def del_address(request, id):
    prod = AddressBook.objects.get(pk=id)
    prod.delete()
    return redirect('chech_out')

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

def payment_product(request, id):
    print("payment product")
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = Cart_Item.objects.filter(carts=cart)
    adds = get_object_or_404(AddressBook, pk=id)
    
    total_price = 0
    try:
        total_price = float(request.session.get('total', cart.get_total_price()))
    except (TypeError, ValueError):
        total_price = 0

    wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'balance': 0})

    flag = 1 if wallet.balance >= total_price else 0

    if request.method == "POST":
        selected_option = request.POST.get('payment')
        if selected_option == "cod":
            return render(request, "cod.html")
        else:
            return render(request, "razorpay.html", {'total_price': total_price * 100})

    context = {
        'adds': adds,
        'sum': total_price,
        'cart_items': cart_items,
        'flag': flag,
    }
    return render(request, 'payment.html', context)


# def payment_product(request, id):
#     print("payment product")
#     cart = Cart.objects.get(user=request.user)
#     cart_items = Cart_Item.objects.filter(carts=cart)
#     adds = AddressBook.objects.get(pk=id)
    
#     total_price = 0
#     #discount_amount = 0
    
#     if (request.session.get('total')):
#             total_price = request.session.get('total')
            
#     else:
#         total_price = cart.get_total_price()
#     try:
#         total_price = float(total_price)
#         wallet = Wallet.objects.get(user=request.user)
        
        
#     except (TypeError, ValueError):
#             wallet = Wallet.objects.create(user=request.user)
#             total_price = 0 
#     print(total_price)
#     # try:
#     #     wallet = Wallet.objects.get(user=request.user)
#     # except:
#     #     wallet = Wallet.objects.create(user=request.user)

    
    
#     if wallet.balance >= sum:
#         flag = 1
#     else:
#         flag = 0
            

#     if request.method == "POST":
    
        
        
#         selected_option = request.POST.get('payment')
#         if selected_option == "cod":
            
#             return render(request,"cod.html")
#         else:
            
#             return render(request,"razorpay.html",{'total_price':total_price*100})
       
#         # calculating sum
#     context = {
#         'adds': adds,
#         'sum': total_price,
#         'cart_items': cart_items,
#         'flag': flag,
       
        
#         }
#     return render(request, 'payment.html', context)


# user profile function
def userprofile(request):
    user=request.user
    address = user.addresses.all()
   
    if address:
        address_added = True
    else:
        address_added = False

    context = {
        
        'address_added': address_added,
        'address': address
    }

    return render(request, 'userprofile.html', context)

#coupon------------------------------------------------------------------/





def apply_coupon(request):
    print('Coupon starts')
    if request.method == 'POST':
        data = {}
        body = json.loads(request.body)
        coupon_code = body.get('coupon')
        total_price = body.get('total_price')
        discount_price = body.get('discount_price')
        

        try:
            coupon = Coupon.objects.get(coupon_code__iexact=coupon_code, is_expired=False)
        except Coupon.DoesNotExist:
            data['message'] = 'Not a Valid Coupon'
            data['total']  = total_price
        else:
            minimum_amount = coupon.minimum_amount
            discount_price = coupon.discount_price
            if total_price >= minimum_amount:
                total_price -= discount_price
                request.session['total'] =total_price
               # data['message'] = f'{coupon.coupon_code} Applied'
                data['message'] = f'₹ {coupon.discount_price} is applied as discount price from coupon code 111'
                
            else:
                data['message'] = 'Not a Valid Coupon'
            data['total'] = total_price
            

        return JsonResponse(data)
    #user side management---------------------------------------------------//
    
def user_add_address(request):
    if request.method == "POST":
        address_form = AddressBookForm(request.POST, request.FILES)
        if address_form.is_valid():
            address = address_form.save(commit=False)  
            address.user = request.user 
            address.save() 
            return redirect("userprofile")  
    else:
        address_form = AddressBookForm()
  
    context = {'address_form': address_form}
    return render(request, 'add_address.html', context)  

def edit_user_address(request, address_id):
    address = get_object_or_404(AddressBook, id=address_id)

    if request.method == "POST":
        address_form = AddressBookForm(request.POST, instance=address)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect("userprofile")
    else:
        address_form = AddressBookForm(instance=address)

    context = {'address_form': address_form}
    return render(request, 'edit_address.html', context)  

def del_user_address(request, id):
    prod = AddressBook.objects.get(pk=id)
    prod.delete()
    return redirect('userprofile')


    
    

