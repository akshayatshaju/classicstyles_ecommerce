from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login as auth_login, authenticate , logout
from django.contrib import messages,auth


from .models import CustomUser
import os
from .models import *
from .forms import  VerifyForm 
from django.contrib.auth.decorators import login_required
from store.models import product, ProductVariant
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

# @login_required
# def verify_code(request):
#     if request.method == 'POST':
#         form = VerifyForm(request.POST)
#         if form.is_valid():
#             code = form.cleaned_data.get('code')
#             if verify.check(request.user.phone, code):
#                 request.user.is_verified = True
#                 request.user.save()
#                 return redirect('index')
#     else:
#         form = VerifyForm()
#     return render(request, 'otp_login.html', {'form': form})

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

def shop(request):
    Prod = product.objects.all
    return render(request,"products.html",{"Prod":Prod})


#otp-----------------------
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
    pro = product.objects.get(pk=id)
    var = ProductVariant.objects.all()
    # size = Size.objects.all()
    # color = Color.objects.all()
    return render(request, 'single.html', {'pro' : pro})    





