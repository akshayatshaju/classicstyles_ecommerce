from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from cart.models import *


from store.models import *
from website.models import *
from order.models import *
from .forms import OrderForm
import datetime



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
                                    try:
                                        
                                            current_order = Order.objects.get(user=current_user)
                                            print(current_order,"current")
                                            if current_order:
                                                    data = current_order
                                            else:
                                                    raise Exception("order not formed")
                                    except Exception as e:
                                             print("exception")
                                             data = Order()
                                    print(1111)
                                    
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
                                        payment_method = Payment.objects.create(user=current_user,payment_method=payment_method_selected,amount_paid=total_price,status=False)
                                        
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
                                        flag=1

                                        
                                        return JsonResponse({'message': 'Order placed successfully','flag':flag})

            return render (request, "payment.html")