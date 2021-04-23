from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType



class User_manager(BaseUserManager):

    #method to create a basic user
    def create_user(self, first_name, last_name, email, phone, password):
        email = self.normalize_email(email)
        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = email,
            phone = phone,
            
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    #different method for creation of a superuser. Very few fields to be entered comparatively
    def create_superuser(self, email, password=None):
        user = self.create_user(
            first_name = "Default",
            last_name = "Superuser",
            email = email,
            phone = "Null",
            password = password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(PermissionsMixin, AbstractBaseUser):

#All the fields that every user will have
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.EmailField(max_length=32, unique=True)
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=511, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_retailer = models.BooleanField(default=False)
    is_wholesaler = models.BooleanField(default=False)
    request_retailer = models.BooleanField(default=False)
    request_wholesaler = models.BooleanField(default=False)
    #For user creation through terminal

    #Username will be used as username field
    USERNAME_FIELD = "email"

    #calling User_manager class
    objects = User_manager()

    #User object can be referenced by string username
    def __str__(self):
        return self.email

    def full_name(self):
        return self.first_name+" "+self.last_name
    #Additional permissions that a user caan have
    class Meta:
            permissions = (("can view dashboard","To open dashboard"),
                ("can view manager level","To open manager dashboard"),
                ("can view staff dashboard","To open staff dashboard"))


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.CharField(max_length=255)
    house = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    locality = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    pincode = models.CharField(max_length=6)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    def __str__(self):
        main = self.house+" "+self.street+" "+self.locality+" "+self.city+" Pin Code:"+self.pincode+" "+self.state
        if self.landmark:
            main = main + " Landmark: "+self.landmark
        return main


#Creating new group objects
p, created = Group.objects.get_or_create(name='retailer')
p, created = Group.objects.get_or_create(name='wholesaler')
p, created = Group.objects.get_or_create(name='merchant')
p, created = Group.objects.get_or_create(name='customer')