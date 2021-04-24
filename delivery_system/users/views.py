from django.shortcuts import render, redirect
from .forms import RegistrationForm, editprofileform, AddressCreateForm, MakeUserWholesalerForm, MakeUserRetailerForm, RetailerRegistrationForm, WholesalerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm, PasswordResetForm
from users.models import User, Address
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.models import Group
from django.http import HttpResponse

@login_required()
def index(request):
    return redirect('shop:product_list')

#Function to check if a user is part of a group
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

#To display register page
def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        group = Group.objects.get(name='customer') 
        group.user_set.add(user)
              
        return redirect('users:login')

    else:
        return render(request, 'register.html', {"form" : form })

def register_as_retailer(request):
    form = RetailerRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        group = Group.objects.get(name='customer') 
        group.user_set.add(user)

        return redirect('users:login')
    else:
        return render(request, 'register-retailer.html', {"form" : form })

def register_as_wholesaler(request):
    form = WholesalerRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()    
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        group = Group.objects.get(name='customer') 
        group.user_set.add(user)
        return redirect('users:login')
    else:
        return render(request, 'register-wholesaler.html', {"form" : form })

@login_required
def profile(request):
    qs = Address.objects.filter(user=request.user)
    context = {
        'details': request.user,
        'addresses': qs
    }
    return render(request, 'profile.html', context)

@login_required
def passwordchange(request):

    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('users:profile')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form':form}
        return render(request, 'edit-password.html', args)

@login_required
def updateprofile(request):
    user = request.user
    if request.method == "POST":
        form = editprofileform(request.POST,instance = user,initial={'email':request.user.email,'phone':request.user.phone})
        form.actual_user = user
        # if form.is_valid():
        form.save()
        return redirect("users:profile")
    else:
        form = editprofileform(initial={'email':request.user.email,
            'first_name': request.user.first_name,
            'last_name':request.user.last_name,
            'phone':request.user.phone,
            })
        args = {'form':form}
        return render(request, 'edit.html', args)

@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('users/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'edit-password.html', {
        'form': form
    })

@login_required
def create_address(request):
    if request.method == "POST":
        form = AddressCreateForm(request.POST)
        if form.is_valid():
            context = Address()
            context.user = request.user
            context.tag = form.cleaned_data['tag']
            context.house = form.cleaned_data['house']
            context.street = form.cleaned_data['street']
            context.locality = form.cleaned_data['locality']
            context.pincode = form.cleaned_data['pincode']
            context.city = form.cleaned_data['city']
            context.state = form.cleaned_data['state']
            context.save()
            return redirect('users:profile')
    form = AddressCreateForm(request.POST or None)
    context = {'form':form}
    return render(request, 'add-address.html', context)

@login_required
def address_details(request, addr_id):
    obj = Address.objects.get(id=addr_id)
    form = AddressCreateForm(request.POST or None, instance=obj)
    if form.is_valid():
        if obj.user==request.user:
            form.save()
    context = {'form':form}
    return render(request, 'update-address.html', context)

@login_required
def address_delete(request, addr_id):
    obj = Address.objects.get(id=addr_id)
    if request.method=='POST':
        obj.delete()
        return redirect('users:profile')
    context = {"address":obj}
    return render(request, 'delete-address.html', context)

@user_passes_test(lambda u: u.is_superuser)
def wholesaler_requests(request):
    qs = User.objects.filter(request_wholesaler=True)
    context={'users':qs}
    return render(request, 'wholesaler_requests.html', context)

@user_passes_test(lambda u: u.is_superuser)
def wholesaler_request_check(request, user_id):
    user = User.objects.get(id=user_id)
    addresses = Address.objects.filter(user=user)
    form = MakeUserWholesalerForm(request.POST or None, instance=user)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            if(user.is_wholesaler):
                group = Group.objects.get(name='wholesaler') 
                group.user_set.add(user)
                group = Group.objects.get(name='merchant') 
                group.user_set.add(user)
                group = Group.objects.get(name='customer') 
                group.user_set.remove(user)
            return redirect('users:wholesaler-requests')

    context={'user':user, 'addresses':addresses, 'form':form}
    return render(request, 'wholesaler_request.html', context)



@group_required('wholesaler')
def retailer_requests(request):
    qs = User.objects.filter(request_retailer=True)
    context={'users':qs}
    return render(request, 'retailer_requests.html', context)


@group_required('wholesaler')
def retailer_request_check(request, user_id):
    user = User.objects.get(id=user_id)
    addresses = Address.objects.filter(user=user)
    form = MakeUserRetailerForm(request.POST or None, instance=user)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            if(user.is_retailer):
                group = Group.objects.get(name='retailer') 
                group.user_set.add(user)
                group = Group.objects.get(name='merchant') 
                group.user_set.add(user)
                group = Group.objects.get(name='customer') 
                group.user_set.remove(user)
            return redirect('users:retailer-requests')

    context={'user':user, 'addresses':addresses, 'form':form}
    return render(request, 'retailer_request.html', context)

@login_required
def select_address(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    if request.method=='POST':
        user.location = request.POST.get('locations')
        user.save()
        return redirect('shop:product_list')
    context = {'addresses':addresses}
    return render(request, 'select_address.html', context)