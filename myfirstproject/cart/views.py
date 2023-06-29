from django.shortcuts import get_object_or_404, render,redirect
from django.views import View
from store.models import product
from cart.models import Cart,Cart_Item
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from website.models import CustomUser, AddressBook
from .forms import   AddressBookForm


@login_required
def add_cart(request):

    print("add to cart request hit")
    try:
        # fetching data
        email = request.user.email
        product_id = request.GET.get('product_id')
        user_instence = CustomUser.objects.get(email = email)

        
        # update cart table
        cart, _ = Cart.objects.get_or_create(user = user_instence)
        
        

        # update cartitem table
        Product_instance = product.objects.get(pk=product_id)

        new_cartitem, item_created = Cart_Item.objects.get_or_create(user = user_instence, carts = cart, product = Product_instance)

        if not item_created and product.quantity > 1:
            Cart_Item.quantity += 1
        Cart_Item.save()
            
       


    
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
    cart = Cart.objects.filter(user=request.user).first()
    cart_items =Cart_Item.objects.filter(carts=cart)
    cart_total = calculate_cart_total(cart_items)
    context = {
        'cart_items' : cart_items,
        'carts' : cart,
        'cart_total': cart_total
    }
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
            cart_item.quantity += 1
        elif action == 'decrease':
            cart_item.quantity -= 1 if cart_item.quantity > 1 else 0
        cart_item.save()

        return JsonResponse({'status': 200, 'quantity': cart_item.quantity, 'subtotal': cart_item.sub_total() })

class chech_out (View):

    def get(self, request):
        cart_items = Cart_Item.objects.filter(user=request.user)
        cart = Cart.objects.get(user=request.user)
        address = AddressBook.objects.filter(user=request.user)
        if cart_items:
            sum = cart.get_total_price()

        context = {
            'cart_items': cart_items,
           
            'address': address,
            'sum':sum
        }

        return render(request, 'checkout.html', context)
    
 


def add_address(request):
    if request.method == "POST":
        address_form = AddressBookForm(request.POST, request.FILES)
        if address_form.is_valid():
            address = address_form.save(commit=False)  
            address.user = request.user 
            address.save() 
            return redirect("chech_out")  
    else:
        address_form = AddressBookForm()
  
    context = {'address_form': address_form}
    return render(request, 'add_address.html', context)

def edit_address(request, address_id):
    address = get_object_or_404(AddressBook, id=address_id)

    if request.method == "POST":
        address_form = AddressBook(request.POST, request.FILES, instance=address)
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect("chech_out")  
    else:
        address_form = AddressBook(instance=address)

    context = {'address_form': address_form}
    return render(request, 'edit_address.html', context)

def del_address(request, id):
    prod = AddressBook.objects.get(pk=id)
    prod.delete()
    return redirect('chech_out')

# def payment_product(request):
#     return render(request, 'payment.html')

def payment_product(request, id):
    cart = Cart.objects.get(user=request.user)
    cart_items =Cart_Item.objects.filter(carts=cart)
    adds = AddressBook.objects.get(pk=id)
    sum = cart.get_total_price()

    context = {
        'adds' : adds,
        'sum' : sum,
        'cart_items': cart
         

    }
    return render(request, 'payment.html', context )

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

