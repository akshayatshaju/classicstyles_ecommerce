

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.http import HttpResponse, HttpResponseRedirect
from website . models import  CustomUser
from store.models import product,Category,ProductVariant
from . forms import ProductForm, CategoryForm, VariantForm

from .forms import Aforms

#from .models import CustomUser

# Create your views here.
@login_required(login_url='admin_login')
def admin_panel(request):
    return render(request, 'admin_template/admin_panel.html')   

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
    




       

