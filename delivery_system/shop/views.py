from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from users.models import Address, User
from .forms import CreateCategoryForm, CreateProductForm, UpdateProductForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth.models import Group

def group_required(group, login_url=None, raise_exception=False):
    def check_perms(user):
        if isinstance(group, str):
            groups =(group, )
        else:
            groups = group
        if user.groups.filter(name__in=groups).exists():
            return True
        if raise_exception:
            raise PermissionDenied
        return False
    return user_passes_test(check_perms, login_url=login_url)


def product_list(request, category_id=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True, sort='retail')
    context = {'categories': categories, 'products': products}
    if category_id:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category, available=True, sort='retail')
        context = {'category':category, 'categories': categories, 'products': products}
    return render(request, 'shop/product/list.html', context)

def wholesale_product_list(request, category_id=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True, sort='wholesale')
    context = {'categories': categories, 'products': products}
    if category_id:
        category = Category.objects.get(id=category_id)
        products = Product.objects.filter(category=category, available=True, sort='wholesale')
        context = {'category':category, 'categories': categories, 'products': products}
    return render(request, 'shop/product/wholesale_list.html', context)




def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    context = {'product': product}
    return render(request, 'shop/product/detail.html', context)


@group_required('merchant')
def category_create(request):
    form = CreateCategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('shop:product_list')
    context={'form':form}
    return render(request, 'shop/product/create_category.html', context)



@group_required('merchant')
def product_create(request):
    if request.user.location==None:
        return redirect('users:set-address')
    form = CreateProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = Product()
        cats = form.cleaned_data['category']
        instance.name = form.cleaned_data['name']
        instance.image = form.cleaned_data['image']
        instance.description = form.cleaned_data['description']
        instance.price = form.cleaned_data['price']
        instance.original_price = form.cleaned_data['original_price']
        instance.available = form.cleaned_data['available']
        instance.stock_units = form.cleaned_data['stock_units']
        instance.seller = request.user
        if request.user.groups.filter(name='wholesaler').exists():
            instance.sort = 'wholesale'
        else:
            instance.sort = 'retail'
        instance.location = request.user.location
        instance.save()
        for cat in cats:
            instance.category.add(cat.id)
        instance.save()
        return redirect('shop:product_list')
    context={'form':form}
    return render(request, 'shop/product/create_product.html', context)

@group_required('merchant')
def product_update(request, product_id):
    instance = get_object_or_404(Product, id=product_id)
    form = UpdateProductForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():# and request.user==instance.seller:
        form.save()
        cats = form.cleaned_data['category']
        instance.category.clear()
        for c in cats:
            instance.category.add(c.id)
        instance.save()
        return redirect('shop:product_list')
    context = {'form':form}
    return render(request, 'shop/product/update_product.html', context)

@group_required('merchant')
def product_delete(request, product_id):
    instance = get_object_or_404(Product, id=product_id)
    if request.method=='POST':
        instance.delete()
        return redirect('shop:product_list')
    context = {'product':instance}
    return render(request, 'shop/product/delete_product.html', context)

@group_required('merchant')
def user_products(request):
    user = request.user
    products = Product.objects.filter(seller=user)
    context = {'products': products}
    return render(request, 'shop/product/user_products.html', context)


def products_by_seller(request, user_id):
    user = get_object_or_404(User, id=user_id)
    products = Product.objects.filter(seller=user)
    context = {'user':user, 'products':products}
    return render(request, 'shop/product/products_by_seller.html', context)

def search_products(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        submitbutton= request.GET.get('submit')
        if query is not None:
            lookups= Q(name__icontains=query)
            results= Product.objects.filter(lookups).distinct()
            context={'results': results,
                     'submitbutton': submitbutton}
            return render(request, 'shop/product/product_search.html', context)
        else:
            return render(request, 'shop/product/product_search.html')
    else:
        return render(request, 'shop/product/product_search.html')