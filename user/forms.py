# from django import forms
# from .models import CustomerProfile
# from .models import TailorProfile

from django import forms
from .models import User, Customer, Tailor, Service
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user
from django.contrib.auth.forms import AuthenticationForm



class CustomerSignupForm(forms.ModelForm):
    # email = forms.EmailField(max_length=25, required=True)
    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'CNIC', 'address', 'phone',
                  'password', 'password2', 'profile_image']
        labels = {
            'username': 'Username', 'first_name': 'First name', 'last_name': 'Last name', 'email': 'Email',
            'CNIC': 'Cnic #', 'address': 'Address', 'phone': 'Phone',
            'password': 'Password', 'password2': 'Confirm password', 'profile_image': 'Profile Image',
        }

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(max_length=25, widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    phone = forms.CharField(max_length=11, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    CNIC = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               required=True)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                required=True)

    profile_image = forms.ImageField(required=False)


    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            self.add_error("password2", "Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = User.Role.CUSTOMER
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        self.clean_password2()
        return cleaned_data



class CustomerLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, max_length=30)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None or not user.is_active or user.role != User.Role.CUSTOMER:
                raise forms.ValidationError("Invalid login credentials.")

    def login(self, request):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        return user






class TailorSignupForm(forms.ModelForm):
    class Meta:
        model = Tailor

        fields = ['username','first_name', 'last_name', 'email', 'CNIC', 'address', 't_physical_shop_address', 'phone','password', 'password2',  'profile_image']
        labels = {
            'username': 'Username', 'first_name': 'First name', 'last_name': 'Last name','email': 'Email',
             'CNIC': 'Cnic #', 'address': 'Address','t_physical_shop_address': 'Shop Address', 'phone': 'Phone',
            'password': 'Password', 'password2': 'Confirm password','profile_image': 'Profile Image',
        }

    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    email = forms.EmailField(max_length=25, widget=forms.EmailInput(attrs={'class': 'form-control'}), required=True)
    address = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    phone = forms.CharField(max_length=11, widget=forms.NumberInput(attrs={'class': 'form-control'}), required=True)
    CNIC = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    t_physical_shop_address = forms.CharField(label='Physical Shop Address',max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    profile_image = forms.ImageField(required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = User.Role.TAILOR
        if commit:
            user.save()
        return user

    def clean(self):
        cleaned_data = super().clean()
        self.clean_password2()
        return cleaned_data


class TailorLoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, max_length=30)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None or not user.is_active or user.role != User.Role.TAILOR:
                raise forms.ValidationError("Invalid login credentials.")

    def login(self, request):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        return user


class ServiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ServiceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Service
        fields = ['service_name', 'service_type', 'service_price', 'service_description', 'service_image']

        labels = {
            'service_type': 'Service Type', 'service_name': 'Service Name','service_price': 'Price', 'service_image': 'Image',
            'service_description': 'Description'
        }

    service_name = forms.CharField(max_length=30)
    service_price = forms.CharField(max_length=7)
    service_type = forms.CharField(max_length=120)
    service_description = forms.Textarea()
    service_image=forms.ImageField(required=False)

    def save(self, commit=True):
        service = super().save(commit=False)
        user = get_user(self.request)
        service.tailor_id = user.id
        service.service_image = service.service_image.path
        if commit:
            service.save()
        return service

