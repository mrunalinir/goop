from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm
#The model for which we are creating form
from .models import User, Address
from django.conf import settings
from django.core.mail import send_mail
import random

#The form that will be rendered and viewed by the website users
class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields =(
            'first_name',
            'last_name',
            'email',
            'phone',           
        )

    # To make sure valid, unique email is entered
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("E-mail id is already taken. Please enter a valid email id")
        return email

    #To make sure valid, unique phone number is entered
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        ps = User.objects.filter(phone=phone)
        if ps.exists():
            raise forms.ValidationError("Phone number is already take. Please enter a unique phone number.")
        if int(phone) and int(phone)>1000000000 and int(phone)<= 9999999999:
            return phone
        else:
            raise forms.ValidationError("Please enter a valid phone number")


    #To verify if both the passwords are same
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and  password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

    #To save user and set the userer password 
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class RetailerRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields =(
            'first_name',
            'last_name',
            'email', 
            'phone', 
            'request_retailer'         
        )

    # To make sure valid, unique email is entered
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("E-mail id is already taken. Please enter a valid email id")
        return email

    #To make sure valid, unique phone number is entered
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        ps = User.objects.filter(phone=phone)
        if ps.exists():
            raise forms.ValidationError("Phone number is already take. Please enter a unique phone number.")
        if int(phone) and int(phone)>1000000000 and int(phone)<= 9999999999:
            return phone
        else:
            raise forms.ValidationError("Please enter a valid phone number")


    #To verify if both the passwords are same
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and  password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

    #To save user and set the userer password 
    def save(self, commit=True):
        user = super(RetailerRegistrationForm, self).save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class WholesalerRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget = forms.PasswordInput)

    class Meta:
        model = User
        fields =(
            'first_name',
            'last_name',
            'email',
            'phone',  
            'request_wholesaler'         
        )

    # To make sure valid, unique email is entered
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("E-mail id is already taken. Please enter a valid email id")
        return email

    #To make sure valid, unique phone number is entered
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        ps = User.objects.filter(phone=phone)
        if ps.exists():
            raise forms.ValidationError("Phone number is already take. Please enter a unique phone number.")
        if int(phone) and int(phone)>1000000000 and int(phone)<= 9999999999:
            return phone
        else:
            raise forms.ValidationError("Please enter a valid phone number")


    #To verify if both the passwords are same
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and  password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")

    #To save user and set the userer password 
    def save(self, commit=True):
        user = super(WholesalerRegistrationForm, self).save(commit=True)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields =(
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_active', 
            'is_staff', 
            'is_blocked', 
            'is_retailer', 
            'is_wholesaler', 
            'request_retailer', 
            'request_wholesaler', 
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()


    class Meta:
        model = User
        fields =(
            'first_name',
            'last_name',
            'email',
            'phone',
            'is_active', 
            'is_staff', 
            'is_blocked', 
            'is_retailer', 
            'is_wholesaler', 
            'request_retailer', 
            'request_wholesaler',
        )

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class changedetails(forms.ModelForm):


    class Meta:
        model = User
        fields =(
            'first_name',
            'last_name',
            'phone',

        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.count()>1:
            raise forms.ValidationError("E-mail id is already taken. Please enter a valid email id")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        ps = User.objects.filter(phone=phone)
        if ps.count()>1:
            raise forms.ValidationError("Phone number is already take. Please enter a unique phone number.")
        if int(phone) and int(phone)>1000000000 and int(phone)<= 9999999999:
            return phone
        else:
            raise forms.ValidationError("Please enter a valid phone number")

 
    def save(self, commit=True):
        user = super(changedetails, self).save(commit=True)
        #user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class editprofileform(changedetails):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    phone = forms.CharField(max_length=10)
    
class AddressCreateForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'tag', 'house', 'street', 'locality', 'landmark', 'pincode', 'city', 'state'
        ]
    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if int(pincode) and int(pincode)>500000 and int(pincode)<600000:
            return pincode
        else:
            raise forms.ValidationError("Please enter a valid pincode")


class MakeUserWholesalerForm(forms.ModelForm):
    # is_wholesaler = forms.BooleanField(label='Make the user a wholesaler?')
    # request_wholesaler = forms.BooleanField(label='Wholesaler request processed?')
    class Meta:
        model = User
        fields = [
            'is_wholesaler', 'request_wholesaler'
        ]
        labels = {
            'is_wholesaler':'Make this user a wholesaler?', 
            'request_wholesaler':'Clear the users wholesaler request?'
        }

class MakeUserRetailerForm(forms.ModelForm):
    # is_wholesaler = forms.BooleanField(label='Make the user a wholesaler?')
    # request_wholesaler = forms.BooleanField(label='Wholesaler request processed?')
    class Meta:
        model = User
        fields = [
            'is_retailer', 'request_retailer'
        ]
        labels = {
            'is_retailer':'Make this user a retailer?', 
            'request_retailer':'Clear the users retailer request?'
        }

class OTPAuthenticationForm(AuthenticationForm):
    otp = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean(self):
        # Allow Django to detect can user log in
        super(OTPAuthenticationForm, self).clean()

        # If we got this far, we know that user can log in.
        if self.request.session.has_key('_otp'):
            if self.request.session['_otp'] != self.cleaned_data['otp']:
                raise forms.ValidationError("Invalid OTP.")
            del self.request.session['_otp']
        else:
            # There is no OTP so create one and send it by email
            # otp = "1234"
            otp=str(random.randint(100000, 999999))
            print(otp)
            send_mail(
                subject="Your OTP Password",
                message="Your OTP password is %s" % otp,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[self.user_cache.email]
            )
            self.request.session['_otp'] = otp
            # Now we trick form to be invalid
            raise forms.ValidationError("Enter OTP you received via e-mail")