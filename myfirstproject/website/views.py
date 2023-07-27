import decimal
from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate , logout
from django.contrib import messages,auth
from django.contrib import messages
from django.db.models import Q
from .models import CustomUser
import os
from .models import *
from .forms import  VerifyForm ,UserProfileForm, PriceFilterForm 
from django.contrib.auth.decorators import login_required
from store.models import *
from order.models import*
from .import verify




# Create your views here.

def home(request):
    
    return render(request,"index.html")



# create signup (register and login)
def register(request):
    email = request.session.get('email')

    if email:
        return redirect('home')
    if request.method == 'POST':
        #form = UserCreationForm(request.POST)

        email = request.POST.get('email')
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if pass1 == pass2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request,'user already exists')
                return redirect('register')
            else:
                user = CustomUser.objects.create_user(email=email, name=name, phone_number=phone_number, password=pass1)
                user.save()
                
                #verify.send(form.cleaned_data.get('phone'))
                

                return redirect('login')
        else:
            messages.info(request,'Password do not match')
            return redirect('register')

    return render(request,'register.html')  

#verification otp



#login

def login(request):
    email = request.session.get('email')

    if email:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass1']
        user = auth.authenticate(email=email,password=password) 
        if user is not None:
            auth.login(request,user)
            request.session['email']=email
            messages.info(request,'Logged in succesfully')
            return redirect("home")

            
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')

    return render(request,'login.html')  

def signout(request):
    logout(request)
    request.session.flush()
    messages.success(request, "logged out succesfuly")
    return redirect('home') 

#shop------------------------------------------------------------------------------------------------//  

def shop(request,category_slug=None):
    
   
    categories = None
    products = None
    price_filter_form = PriceFilterForm(request.GET or None)
    
    
    

    if category_slug != None:
        categories = get_object_or_404(Category, slug= category_slug)
        
        

        products = ProductVariant.objects.filter(product_name__category=categories)

    else:   
         
    
            products = ProductVariant.objects.all()
            categories = Category.objects.all()
    print(products)
    return render(request,"products.html",{"Prod":products,"price_filter_form":price_filter_form})

def price_filter(request):
    price_filter_form = PriceFilterForm(request.GET or None)
    product = ProductVariant.objects.all()
    
    if price_filter_form.is_valid():
        min_price = price_filter_form.cleaned_data['min_price']
        max_price = price_filter_form.cleaned_data['max_price']
        product = [p for p in product if min_price <= p.price <= max_price]
        print(product)
    return render(request,"price_filter.html",{"Prod":product,"price_filter_form":price_filter_form})    

#otp-----------------------------------------------------------------------------------------------------//
# otp verification
# @login_required
def verify_code(request):
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('code')
            phone_no = request.session.get('phone')
            
            
            if verify.check(phone_no, code):
                print("checked")
                
                user = CustomUser.objects.get(email= request.session.get('username'))
                userobj = CustomUser.objects.filter(email = request.session.get('username'))
                print(user)
                print(user.is_authenticated)
                print(user.is_active)
                print(user.is_superuser)
                if userobj is not None and user.is_active and user.is_superuser == False:
                    print(user.is_authenticated)
                    auth_login(request, user)
                    return redirect(home)
                print(user)
                return redirect(home)
            else:
                print("error")
    else:
        form = VerifyForm()
    return render(request, 'verifyotp.html', {'form': form})


def phone_verify(request):
    print("oohe")
    if request.method == "POST":
        print("hhe")
        phone = '+91'+  str(request.POST['phone_number'])
        if check_phone_number(request.POST['phone_number']):
            verify.send(phone)
            user = username_password(request.POST['phone_number'])
            request.session['username'] = user.email
            print(user.email)
            user.is_verified = True
            user.is_active = True
            request.session['phone'] = phone
            return redirect(verify_code)
        else:
            context = "Please register first"
            return render(request, 'phone_verify.html',{'context':context})
    return render(request, 'phone_verify.html')

def username_password(phone):
    user = CustomUser.objects.filter(phone_number=phone)[0]
    return user

def check_phone_number(phone_number):
    
    try:
        phone_number = CustomUser.objects.filter(phone_number=phone_number)[0]
        return True
    except CustomUser.DoesNotExist:
        return False
    

def single_details(request, id):
    pro = ProductVariant.objects.get(pk=id)
    var = ProductVariant.objects.all()
    
    return render(request, 'single.html', {'pro' : pro})    


#search----------------/



def search_brand(request):
    print('searching partialy')
    if request.method == 'POST':
        print('uwhkh')
        query = request.POST.get('search')
        variants = product.objects.filter(product_name__icontains=query)
        print(variants)
        return render(request, "search_brand.html", {'variants': variants})

# from fuzzywuzzy import fuzz

# def search_brand(request):
#     print('searching partially')
#     if request.method == 'POST':
#         print('uwhkh')
#         query = request.POST.get('search')

#         # Filter products that partially match the search query
#         variants = product.objects.filter(product_name__icontains=query)

#         # Search for similar products using FuzzyStringMatcher
#         similarity_threshold = 80  # You can adjust this threshold as per your requirements
#         similar_variants = []

#         for variant in variants:
#             similarity_score = fuzz.partial_ratio(query, variant.product_name)
#             if similarity_score >= similarity_threshold:
#                 similar_variants.append((variant, similarity_score))

#         # Sort similar variants by similarity score (descending order)
#         similar_variants.sort(key=lambda x: x[1], reverse=True)

#         return render(request, "search_brand.html", {'variants': similar_variants})

    
    
#order listing---------------------/    

# @login_required(login_url='signin')
def orderlist(request):
    
    order = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(request, 'orderlist.html',{'order': order})

@login_required
def create_user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('profile')  # Replace 'profile' with your profile URL name
    else:
        form = UserProfileForm()
    
    return render(request, 'create_user_profile.html', {'form': form})


#forgot password------------------------------------------------------/
def forgotPassword(request):
    global mobile_number_forgotPassword
    print('ugfug')
    if request.method == 'POST':
        # setting this mobile number as global variable so i can access it in another view (to verify)
        mobile_number_forgotPassword = request.POST.get('phone_number')
        print(mobile_number_forgotPassword)
        # checking the null case
        if mobile_number_forgotPassword is '':
            
            messages.warning(request, 'You must enter a mobile number')
            print('number')
            return redirect('forgotPassword')
   
        # instead we can also do this by savig this mobile number to session and
        # access it in verify otp:
        # request.session['mobile']= mobile_number
        user = CustomUser.objects.filter(phone_number=mobile_number_forgotPassword)
        print(user)
        if user:  #if user exists
            verify.send('+91' + str(mobile_number_forgotPassword))
            print('otp')
            return redirect('forgotPassword_otp')
        else:
            messages.warning(request,'Mobile number doesnt exist')
            return redirect('forgotPassword')
            
    return render(request, 'forgotPassword.html')


def forgotPassword_otp(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('code')
        # otp = request.POST.get('otp')
        if verify.check('+91'+ str(mobile_number), otp):
            user = CustomUser.objects.get(phone_number=mobile_number)
            if user:
                return redirect('resetPassword')
        else:
            messages.warning(request,'Invalid OTP')
            return redirect('enter_otp')
    else:
        form = VerifyForm()
        
    return render(request,'forgotPassword_otp.html', {'form':form})


def resetPassword(request):
    mobile_number = mobile_number_forgotPassword
    
    if request.method == 'POST':
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirm_password')
        print(str(password1)+' '+str(password2)) #checking
        
        if password1 == password2:
            user = CustomUser.objects.get(phone_number=mobile_number)
            print(user)
            print('old password  : ' +str(user.password))
            
            user.set_password(password1)
            user.save()

            print('new password  : ' +str(user.password))
            messages.success(request, 'Password changed successfully')
            return redirect('login')
        else:
            messages.warning(request, 'Passwords doesnot match, Please try again')
            return redirect('resetPassword')
    
    return render(request, 'resetPassword.html')

#cancel order------------------------------------------------------------------------//

def user_order_products(request, id):
    orders = Order.objects.get(pk=id)
    myorder = OrderProduct.objects.filter(order=orders)
    print()
    context = {
        'orders': orders,
        'myorder':myorder
    }
    return render(request, 'userordermanage.html', context)


   
#cancel order----------------------------------------------------------------------/
    
def cancel_order(request,id):
    print(id)
    if request.method == "POST":
        cancellation_reason = request.POST.get('cancellation_reason')
        print(cancellation_reason)
        try:
        
            order = get_object_or_404(Order, pk=id, user=request.user)
            orders = OrderProduct.objects.filter(order=order)
            print(orders)
            print(order)
            order.status = 'Cancelled'
            order.cancellation_reason = cancellation_reason
            order.save()
            if order.status == 'Cancelled':
                for ProductVariant in orders:
                    ProductVariant.quantity += ProductVariant.quantity
                    ProductVariant.save()
                    print('jfguefv')
                    
            if order.payment.payment_method =='razorpal':
                print('walletamount')
                wallet, _ =Wallet.objects.get_or_create(user=request.user)
               
                refund_amount=decimal.Decimal(order.order_total)
                print(refund_amount)
                wallet.balance += refund_amount
                wallet.save()  
                
                     

        except Order.DoesNotExist:
            pass
    return redirect("orderlist")




#return ordr---------------------------------------------------------------------------/

def return_order(request,id):
    print(id)
    if request.method == "POST":
        return_reason = request.POST.get('return_reason')
        try:
        
            order = get_object_or_404(Order, pk=id, user=request.user)
            order.status = 'Cancelled'
            order.return_reason = return_reason
            order.save()
            
            if order.payment.payment_method == 'razorpal' or 'COD':
                wallet, _ = Wallet.objects.get_or_create(user=request.user)
                refund_amount = decimal.Decimal(order.order_total)
                print(refund_amount)
                wallet.balance += refund_amount
                wallet.save()


        except Order.DoesNotExist:
            pass
    return redirect("orderlist")

#wallet-------------------------------------------------------------/

def wallet(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
        if wallet:
            print(wallet.balance)
    except:
        wallet = Wallet.objects.create(user=request.user, balance=0)
    return render(request,'wallet.html',{'wallet':wallet})







