

import datetime
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseRedirect
from website . models import  CustomUser
from store.models import product,Category,ProductVariant,Coupon
from . forms import ProductForm, CategoryForm, VariantForm,CouponForm
from order.models import *
import calendar
from django.db.models.functions import ExtractMonth,ExtractYear,ExtractDay
from django.db.models import Count
from .forms import Aforms


#from .models import CustomUser

# Create your views here.
@login_required(login_url='admin_login')
def admin_panel(request):
    return render(request, 'admin_template/admin_panel.html')   



# from django.db.models import Count, F
# from django.db.models.functions import ExtractMonth, ExtractYear
# import calendar

def dashboard(request):
  
    today = datetime.date.today()
    
    delivered_orders = Order.objects.filter(status='Delivered')
    
    delivered_orders_by_months = delivered_orders.annotate(
        delivered_month=ExtractMonth('created_at'),
        delivered_day=ExtractDay('created_at')
    ).values('delivered_month', 'delivered_day').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_day', 'delivered_count')
    
    delivered_orders_month = []
    delivered_orders_number = []
    for d in delivered_orders_by_months:
        month_name = calendar.month_name[d['delivered_month']]
        day_number = d['delivered_day']
        delivered_orders_month.append(f"{month_name} {day_number}")
        delivered_orders_number.append(d['delivered_count'])

    order_by_months = Order.objects.annotate(
        month=ExtractMonth('created_at'),
        day=ExtractDay('created_at')
    ).values('month', 'day').annotate(count=Count('id')).values('month', 'day', 'count')
    
    monthNumber = []
    dayNumber = []
    totalOrders = []
    for o in order_by_months:
        month_name = calendar.month_name[o['month']]
        day_number = o['day']
        monthNumber.append(f"{month_name} {day_number}")
        dayNumber.append(day_number)
        totalOrders.append(o['count'])

    delivered_orders_by_years = delivered_orders.annotate(delivered_year=ExtractYear('created_at')).values('delivered_year').annotate(delivered_count=Count('id')).values('delivered_year', 'delivered_count')
    delivered_orders_year = []
    delivered_orders_year_number = []
    for d in delivered_orders_by_years:
        delivered_orders_year.append(d['delivered_year'])
        delivered_orders_year_number.append(d['delivered_count'])
    
    order_by_years = Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')
    yearNumber = []
    totalOrdersYear = []
    for o in order_by_years:
        yearNumber.append(o['year'])
        totalOrdersYear.append(o['count'])
   
    
    context ={
        'delivered_orders': delivered_orders,
        'order_by_months': order_by_months,
        'monthNumber': monthNumber,
        'dayNumber': dayNumber,
        'totalOrders': totalOrders,
        'delivered_orders_number': delivered_orders_number,
        'delivered_orders_month': delivered_orders_month,
        'delivered_orders_by_months': delivered_orders_by_months,
        'today': today,
        'order_by_years': order_by_years,
        'yearNumber': yearNumber,
        'totalOrdersYear': totalOrdersYear,
        'delivered_orders_year': delivered_orders_year,
        'delivered_orders_year_number': delivered_orders_year_number,
        'delivered_orders_by_years': delivered_orders_by_years,
        
        
    }
    return render(request, 'admin_template/dashboard.html', context)



# def dashboard(request):
#     orders=Order.objects.get(pk=58)
#     print(orders.created_at)
#     delivered_orders = Order.objects.filter(status='Delivered')
#     delivered_orders_by_months = delivered_orders.annotate(delivered_month=ExtractMonth('created_at')).values('delivered_month').annotate(delivered_count=Count('id')).values('delivered_month', 'delivered_count')
#     print( delivered_orders_by_months)
#     delivered_orders_month = []
#     delivered_orders_number = []
#     for d in delivered_orders_by_months:
#          delivered_orders_month.append(calendar.month_name[d['delivered_month']])
#          delivered_orders_number.append(list(d.values())[1])


    
    

#     order_by_months = Order.objects.annotate(month=ExtractMonth('created_at')).values('month').annotate(count=Count('id')).values('month', 'count')
#     monthNumber = []
#     totalOrders = []
#     print(order_by_months)
   

#     for o in order_by_months:
#         monthNumber.append(calendar.month_name[o['month']])
#         totalOrders.append(list(o.values())[1])
        
#     order_by_year = Order.objects.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id')).values('year', 'count')

#     yearNumber = []
#     total_Orders = []

#     for o in order_by_year:
#         yearNumber.append(o['year'])
#         total_Orders.append(o['count'])    

#     context = {
#         'monthNumber': monthNumber,
#         'totalOrders': totalOrders,
#         'yearNumber': yearNumber,
#         'total_Orders': total_Orders,
#         'delivered_orders':delivered_orders,
#         'order_by_months':order_by_months,
        
#         'totalOrders':totalOrders,
#         'delivered_orders_number':delivered_orders_number,
#         'delivered_orders_month':delivered_orders_month,
#         'delivered_orders_by_months':delivered_orders_by_months,

#     }
    

#     return render(request, 'admin_template/dashboard.html', context)


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin_panel')

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['Password']
        user = authenticate(email=email,password=password)

        if user.is_superuser:
            login(request,user)
            return redirect("admin_panel")
        else:
            messages.error(request,"User name or password is incorect")
            return redirect('admin_login')
    return render(request,"admin_template/admin_login.html")

def admin_logout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "logged out succesfully")
    return redirect('admin_login')

def user(request):
   
    if request.method=="POST":
        fm = Aforms(request.POST)
        if fm.is_valid():
           
            fm.save()
            
            fm = Aforms()
    else:
        fm = Aforms()
    
    stud=CustomUser.objects.all()
    return render(request,'admin_template/user.html',{'fm':fm,'stud':stud})

#user-------------------------------------------------------------------/
def block_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = False
        user.save()
        return redirect('user')

def unblock_user(request, id):
    if request.method == "POST":
        user = CustomUser.objects.get(pk=id)
        user.is_active = True
        user.save()
        return redirect('user')

#product---------------------------------------------------------------------------------------/

def Product_list(request):
    pro = product.objects.all()
    context = {
        'pro' : pro
    }
    return render(request,'admin_template/product.html', context)

def edit_product(request, id):
    Product = get_object_or_404(product, pk=id)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=Product)
        if form.is_valid():
            form.save()
            return redirect('Product_list')
    else:
        form = ProductForm(instance=Product)

    context = {
        "form": form
    }
    return render(request, 'admin_template/edit_product.html', context)


# def del_product(request, id):
#     if request.method == "POST":
#         prod = product.objects.get(pk=id)
#         prod.delete()
#         return redirect('Product_list')

def del_product(request, id):
    Product = get_object_or_404(product, pk = id)
    if request.method == "POST":
        prod = product.objects.get(pk = id)
        prod.delete()
        return redirect('Product_list')

def add_product(request):
    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
     
        if product_form.is_valid():
          
            product_form.save()
          
            
            return redirect("Product_list")
    else:
        product_form = ProductForm()
      
    
    context = {'product_form': product_form, }

    return render(request, 'admin_template/add_product.html', context)



# category---------------------------------------------------------------------------------------------------------------------------/

def category_list(request):
    cat = Category.objects.all()
    context = {
        'cat' : cat
    }
    return render(request,'admin_template/category.html',context)

def del_category(request, id):
    if request.method == "POST":
        prod = Category.objects.get(pk=id)
        prod.delete()
        return redirect('category_list')
    
def edit_category(request, id):
    Product = get_object_or_404(Category, pk=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=Product)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=Product)

    context = {
        "form": form
    }
    return render(request, 'admin_template/edit_category.html', context)    


#productvarient--------------------------------------------------------/
def product_variant(request):
    pro = ProductVariant.objects.all()
    context = {
        'pro' : pro
    }
    return render(request, 'admin_template/product_variant.html', context)

def del_product_variant(request, id):
    if request.method == "POST":
        prod = ProductVariant.objects.get(pk=id)
        prod.delete()
        return redirect('product_variant')

def add_product_variant(request):
    if request.method == "POST":
        productvariant_form = VariantForm(request.POST,request.FILES)
        # image_form = ProductImageFormSet(request.POST, request.FILES, instance=product())
        if productvariant_form.is_valid():
            # myproduct = product_form.save(commit=False)
            productvariant_form.save()
            # image_form.instance = myproduct
            # image_form.save()
            # return redirect('products')
            return redirect("product_variant")
    else:
       productvariant_form = VariantForm()
        # image_form = ProductImageFormSet(instance=product())
    context = {'productvariant_form':productvariant_form}
    return render(request, 'admin_template/add_productvarient.html', context)

def edit_product_variant(request, id):
    product = get_object_or_404(ProductVariant, pk=id)
    if request.method == "POST":
        product_form = VariantForm(request.POST, request.FILES, instance=product)
        if product_form.is_valid():
            product_form.save()
            return redirect('product_variant')
    else:
        product_form = VariantForm(instance=product)

    context = {
        "product_form": product_form
    }
    return render(request, 'admin_template/product_variant_edit.html', context)
#orders-------------------------------------------------------/
    

def orders(request):
    orders = Order.objects.all().order_by("-created_at")
    return render(request, 'admin_template/admin_myorder.html', {'orders':orders})


def edit_order(request, id):
    if request.method == "POST":
        status = request.POST.get("status")
        try:
            order = Order.objects.get(pk=id)
            order.status = status
            order.save()
            if status == 'Delivered':
                payment = order.payment
               
                payment.status = 'Success'
                payment.save()


        except Order.DoesNotExist:
            pass
    return redirect("orders")


#fetch each products from order
def order_products(request, id):
    orders = Order.objects.get(pk=id)
    myorder = OrderProduct.objects.filter(order=orders)
    print()
    context = {
        'orders': orders,
        'myorder':myorder
    }
    return render(request, 'admin_template/ordermanage.html', context)

#coupon------------------------------------------------------------------------------------/

def coupen_manage(request):
    coupens = Coupon.objects.all()
    context = {
        "coupens" : coupens
    }
    return render(request,'admin_template/coupon.html', context)



def add_coupons(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupen_manage')
    else:
        form = CouponForm()

    context = {'form': form}
    return render(request, 'admin_template/add_coupon.html', context)



def del_coupons(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        coup.delete()
    return redirect('coupen_manage')


def edit_coupons(request,id):
    if request.method == "POST":
        coup = Coupon.objects.get(id=id)
        form = CouponForm(request.POST, instance=coup)
        if form.is_valid:
            form.save()
        return redirect('coupen_manage')
    else:
        coup = Coupon.objects.get(id=id)
        form = CouponForm(instance=coup)
        context = {
            "form" : form
        }
    return render(request, 'admin_template/edit_coupon.html', context) 

#Search days----------------------------/


    
# def sales_date(request):
#     if request.method == 'POST':
#         from_date = request.POST.get('fromDate')
#         to_date = request.POST.get('toDate')
#     orders = Orders.objects.filter(created_at__range=[from_date, to_date])
#     total_amount = sum(order.order_total for order in orders)
#     context= {
#         'total_payment_amount': total_amount,
#         'orders': orders
#     }
#     return render(request,'admin/sales-report.html',context)    




       

