from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from cart.models import *

from store.models import *
from website.models import *
from order.models import *
from .forms import OrderForm
import datetime
import razorpay
from django.conf import settings
import json
from django.http import JsonResponse
from cart.models import Cart,Cart_Item


def confirm_order(request):

    print("reauest hit")
    selected_option = request.GET.get('payment')
    print(selected_option)
    return HttpResponse("rest")

# def code_order(request):
#         return render(request, 'cod.html')

    


<<<<<<< HEAD
# def place_order(request):
            
#             print("place order")
#             current_user = request.user
#             flag =0
#             # if cart count is less than or equal to zero redirect back to homepage
#             cart = Cart.objects.get(user=current_user)
#             cart_items = Cart_Item.objects.filter(user=current_user)
#             cart_count = cart_items.count()
#             print(cart_count)
#             if cart_count <= 0:
#                     return redirect('homepage')
#             else:
#                     print("else")
#                     total_price = cart.get_total_price()
#                     if request.method == 'GET':
#                                     try:
                                        
#                                             current_order = Order.objects.get(user=current_user)
#                                             print(current_order,"current")
#                                             if current_order:
#                                                     data = current_order
#                                             else:
#                                                     raise Exception("order not formed")
#                                     except Exception as e:
#                                              print("exception")
#                                              data = Order()
#                                     print(1111)
                                    
#                                     data.user = current_user
#                                     selected_option = request.GET.get('selectedOption')
#                                     payment_method_mapping = {
#                                                 'cod': 'COD',
#                                                 'paypal': 'Paypal',
#                                                 # Add more mappings as needed
#                                             }
#                                     print(selected_option)
#                                     payment_method_selected = payment_method_mapping.get(selected_option)
#                                     print(payment_method_selected)
#                                     if selected_option == 'cod':
#                                         print("first one")
#                                         payment_method = Payment.objects.create(user=current_user,payment_method=payment_method_selected,amount_paid=total_price,status=False)
=======
def place_order(request):
      
        print("place order")
        current_user = request.user
        flag =0
            # if cart count is less than or equal to zero redirect back to homepage
        cart = Cart.objects.get(user=current_user)
        cart_items = Cart_Item.objects.filter(user=current_user)
        cart_count = cart_items.count()
        print(cart_count)
        if cart_count <= 0:
                
                return redirect('homepage')
        else:
                
                print("else")
                total_price = cart.get_total_price()
                if request.method == 'GET':
                        
                                  
                                    data = Order()
                                   
                                    
                                    data.user = current_user
                                    selected_option = request.GET.get('selectedOption')
                                    payment_method_mapping = {
                                                'cod': 'COD',
                                                'paypal': 'Paypal',
                                                # Add more mappings as needed
                                            }
                                    print(selected_option)
                                    payment_method_selected = payment_method_mapping.get(selected_option)
                                    print(payment_method_selected)
                                    if selected_option == 'cod':
                                        print("first one")
                                        payment_method = Payment.objects.create(user=current_user,payment_method='cod',amount_paid=total_price,status="Pending")
>>>>>>> 26be664ff2e5f3571244736f4949380e03955267
                                        
#                                         data.payment = payment_method
#                                         data.first_name = request.GET.get('first')
#                                         data.address_line_1 = request.GET.get('address_line_1')
#                                         data.city = request.GET.get('city')
#                                         data.state = request.GET.get('state')
#                                         data.Pincode = request.GET.get('Pincode')
#                                         data.country = request.GET.get('country')
#                                         data.Phone = request.GET.get('Phone')
#                                         data.Email = request.GET.get('Email')
                                        
                                        
                                        
<<<<<<< HEAD
#                                         data.order_total = total_price
#                                         print(data.user,data.payment,data.address_1,data.order_total)
#                                         data.save()
#                                         print(data)
#                                         # generate order number
#                                         yr = int(datetime.date.today().strftime('%Y'))
#                                         dt = int(datetime.date.today().strftime('%d'))
#                                         mt = int(datetime.date.today().strftime('%m'))
#                                         d = datetime.date(yr,mt,dt)
#                                         current_date = d.strftime("%Y%m%d")
#                                         order_number= current_date + str(data.id)
#                                         data.order_number = order_number
#                                         print(data.order_number,current_date)
#                                         data.save()
#                                         flag=1
=======
                                        data.order_total = total_price
                                        print(data.user,data.payment,data.address_1,data.order_total)
                                        data.save()
                                        print(data)
                                        # generate order number
                                        yr = int(datetime.date.today().strftime('%Y'))
                                        dt = int(datetime.date.today().strftime('%d'))
                                        mt = int(datetime.date.today().strftime('%m'))
                                        d = datetime.date(yr,mt,dt)
                                        current_date = d.strftime("%Y%m%d")
                                        order_number= current_date + str(data.id)
                                        data.order_number = order_number
                                        print(data.order_number,current_date)
                                        data.save()
                    
                            
                            
                                        for item in cart_items:
                                                 
                                                order_product = OrderProduct.objects.create(
                                                                order=data,
                                                                payment=payment_method,
                                                                ProductVariant=item.product_variant,
                                                                quantity=item.quantity,
                                                                price=item.product_variant.price,
                                                                ordered=True
                                                        )
                                                print(order_product)
                                                varient=item.product_variant
                                                varient.stock -= item.quantity
                                                varient.save() 
                                                
                                               
>>>>>>> 26be664ff2e5f3571244736f4949380e03955267

                                                flag=1
                                                 #delete cart items after order is placed
                cart_items.delete()
                if 'total' in request.session:
                        del request.session['total']
                                       
                                    
                                                            
                                        
<<<<<<< HEAD
#                                         return JsonResponse({'message': 'Order placed successfully','flag':flag})

#             return render (request, "payment.html")
=======
        redirect_url = reverse('complete_payment') 
        
        return JsonResponse({'message': 'Order placed successfully.','flag':flag,'id':order_number,'amount':total_price,'redirect':redirect_url})

        # return render (request, "cod.html")
        
        




def place_order_razorpay(request):
    current_user = request.user
    flag = 0

    cart = Cart.objects.get(user=current_user)
    cart_items = Cart_Item.objects.filter(user=current_user)
    
    cart_count = cart_items.count()

    if cart_count <= 0:
        return redirect('homepage')
    else:
        total_price = cart.get_total_price()
        
        if request.method == 'GET':
            
            data = Order()

            data.user = current_user
            selected_option = request.GET.get('selectedOption')
            payment_method_mapping = {
                'razorpal': 'RAZORPAY',
                # Add more mappings as needed
            }
            print(selected_option)
            payment_method_selected = payment_method_mapping.get(selected_option)
            print(payment_method_selected)
            if selected_option == 'razorpal':
                print("fourth one")
                payment_method = Payment.objects.create(
                    user=current_user,
                    payment_method='razorpal',
                    amount_paid=str(total_price),  # Convert Decimal to string
                    status="Success"
                )

                data.payment = payment_method
                data.first_name = request.GET.get('first')
                data.address_line_1 = request.GET.get('address_line_1')
                data.city = request.GET.get('city')
                data.state = request.GET.get('state')
                data.Pincode = request.GET.get('Pincode')
                data.country = request.GET.get('country')
                data.Phone = request.GET.get('Phone')
                data.Email = request.GET.get('Email')
                data.order_total = total_price
                
                print(data.user,data.payment,data.address_1,data.order_total)

                data.save()

                # Generate order number
                current_date = datetime.date.today().strftime('%Y%m%d')
                order_number = current_date + str(data.id)
                data.order_number = order_number
                print(data.order_number,current_date)
                data.save()
                order_id = data.id

                for item in cart_items:
                    order_product = OrderProduct.objects.create(
                        order=data,
                        payment=payment_method,
                        ProductVariant=item.product_variant,
                        quantity=item.quantity,
                        price=item.product_variant.price,
                        ordered=True
                    )
                print(order_product)
                if 'total' in request.session:
                    del request.session['total']
                
                flag = 1
                
                #delete cart items after order is placed
                cart_items.delete()
                cart.delete()
                varient=item.product_variant
                varient.stock -= item.quantity
                varient.save() 


    client = razorpay.Client(auth=(settings.KEY, settings.SECRET))
    print("key")
    payment = client.order.create({
        'amount': int(total_price * 100),  # Convert Decimal to integer in paise/cents
        'currency': 'INR',
        'payment_capture': 1
    })
    cart.razor_pay_order_id=payment['id']
    cart.save()
    print('*****************')
    print(payment)
    amounts=payment['amount']
    ids=payment['id']
    print('*****************')

    cart_data = {
        'cart_id': cart.cart_id,
        # Add other cart attributes as needed
    }

    context = {'cart': cart_data, 'payment': payment,'amounts':amounts,'ids':ids,'order_id':order_id}

    return JsonResponse({'message': 'Order placed successfully', 'flag': flag, 'context': context})

        
        
        
def complete_payment(request):
        id = request.GET.get('id')
        print(id)
        payment_id = request.GET.get('razorpay_payment_id')
        print(payment_id)
        
        total_price = request.GET.get('total_price')
        cart = Cart.objects.filter(user=request.user).first()
        
        print('hggrefjsdbf')
      
        payment_method = request.GET.get('payment_method')
        address = AddressBook.objects.filter(user=request.user)
        cart_items =Cart_Item.objects.filter(carts=cart)
        
      
        context = {
                'id': id,
                'payment_id': payment_id,
                'total_price' : total_price,
                'payment_method': payment_method,
                'cart_items' : cart_items,
                'address': address
                
        }

        return render(request, "order-complete.html", context)     
    
    

       


def wallet_pay(request):
          
        current_user = request.user
        wallet = Wallet.objects.get(user=current_user)
        cart = Cart.objects.get(user=current_user)
        cart_items = Cart_Item.objects.filter(user=current_user)
        cart_count = cart_items.count()
        total_price = cart.get_total_price()
        
                
            
          # if cart count is less than or equal to zero redirect back to homepage
        if cart_count <= 0:
                return redirect('homepage')
        else:        
               
                data = Order()

                data.user = current_user

                payment_method = Payment.objects.create(user=current_user,payment_method='Wallet',amount_paid=total_price,status=False)
                
                data.payment = payment_method
                
                default_address_id = request.GET.get('defaultAddressId')
                print(default_address_id)
                data.first_name = request.GET.get('first')
                data.address_line_1 = request.GET.get('address_line_1')
                data.city = request.GET.get('city')
                data.state = request.GET.get('state')
                data.Pincode = request.GET.get('Pincode')
                data.country = request.GET.get('country')
                data.Phone = request.GET.get('Phone')
                data.Email = request.GET.get('Email')
                
                data.order_total = total_price
                
                data.save()
                print(data)
                # generate order number
                yr = int(datetime.date.today().strftime('%Y'))
                dt = int(datetime.date.today().strftime('%d'))
                mt = int(datetime.date.today().strftime('%m'))
                d = datetime.date(yr,mt,dt)
                current_date = d.strftime("%Y%m%d")
                order_number= current_date + str(data.id)
                data.order_number = order_number
                print(data.order_number,current_date)
                data.save()
                
                for item in cart_items:
                    order_product = OrderProduct.objects.create(
                        order=data,
                        payment=payment_method,
                        ProductVariant=item.product_variant,
                        quantity=item.quantity,
                        price=item.product_variant.price,
                        ordered=True
                    )
                print(order_product)
                if 'total' in request.session:
                    del request.session['total']
                
                flag = 1
                
                #delete cart items after order is placed
                cart_items.delete()
                cart.delete()
                        
                cart.coupon = None
                cart.save()
                wallet.balance = float(wallet.balance) - float(total_price)
                wallet.save()
                redirect_url = reverse('complete_payment') + f'?amount={total_price}&order_number={order_number}&payment_id={payment_method.id}'
                return JsonResponse({'message': 'Order placed successfully.','id':order_number,'amount':total_price,'redirect':redirect_url})
            
>>>>>>> 26be664ff2e5f3571244736f4949380e03955267
