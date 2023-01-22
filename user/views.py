from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .forms import CustomerSignupForm, TailorSignupForm, CustomerLoginForm, TailorLoginForm
from .models import Customer, Tailor
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import uuid
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage




def home(request):
    return render(request,'home.html')

def aboutus(request):
    return render(request,'aboutus.html')
def contactus(request):
    return HttpResponse("Hello miss world")
def termsandconditions(request):
    return render(request, 'termsandconditions.html')

def findtailor(request):
    tailors = Tailor.objects.all()
    context = {'tailors': tailors}
    return render(request, 'Findtailor.html', context)


def findopportunities(request):
    return render(request, 'findopportunities.html')

def login_page(request):
    return render(request, 'login.html')


def token_send(request):
    return render(request,'token_send.html')

def success(request):
    return render(request,'success.html')


def verify_customer(request, auth_token):
    try:
        user_object = Customer.objects.filter(auth_token=auth_token).first()
        if user_object:
            if user_object.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('customer_login')
            else:
                user_object.is_active = True
                user_object.is_verified = True
                user_object.save()
                messages.success(request, 'Your account has been verified.')
                return redirect('customer_login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')

def verify_tailor(request, auth_token):
    try:
        user_object = Tailor.objects.filter(auth_token=auth_token).first()
        if user_object:
            if user_object.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('tailor_login')
            else:
                user_object.is_active = True
                user_object.is_verified = True
                user_object.save()
                messages.success(request, 'Your account has been verified.')
                return redirect('tailor_login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')


def signup_page(request):
    return render(request, 'signup.html')


def tailor_register(request):
    if request.method == 'POST':
        form = TailorSignupForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            email_exists = Tailor.objects.filter(email=email).exists()
            print("Email exist: ", email_exists)
            if email_exists:
                form.add_error('email', 'Email already exists')
                return render(request, 'tailor_register.html', {'form': form})

            else:
                # create a new user

                user = Tailor.objects.create_user(
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    CNIC=form.cleaned_data['CNIC'],
                    address=form.cleaned_data['address'],
                    phone=form.cleaned_data['phone'],
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    password2=form.cleaned_data['password2'],
                    profile_image = request.FILES['profile_image'],
                    t_physical_shop_address=form.cleaned_data['t_physical_shop_address'],
                )

                #Add profile picture to the storage
                if 'profile_image' in request.FILES:
                    profile_image = request.FILES['profile_image']
                    user.profile_image = profile_image

                    fs = FileSystemStorage()
                    filename = fs.save(user.profile_image.name, user.profile_image)
                    user.profile_image = fs.url(filename)
                    user.save()
                else:
                    print("\n*******************else block \n")
                    user.profile_image = './static/assets/profile_img/default.jpg'


                # generate a unique verification token
                token = str(uuid.uuid4())
                # store the token in the user's profile
                user.auth_token = token

                #tailor data saved in database
                user.save()

                # send the verification email
                verification_link = request.build_absolute_uri(reverse('verify_tailor', kwargs={'auth_token':token}))

                send_mail(
                    'Verify your email address',
                    f'Please click the link to verify your email address: {verification_link}',
                    'sewccess3@gmail.com',
                    [user.email],
                    fail_silently=False,
                )
                return redirect('token_send')

    else:
        form = TailorSignupForm()
    return render(request, 'tailor_register.html', {'form': form})

def customer_register(request):
    if request.method == 'POST':
        form = CustomerSignupForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            email_exists = Customer.objects.filter(email=email).exists()
            if email_exists:
                messages.error(request, 'Email already exists')
                return redirect('customer_register')

            else:
                # create a new user
                user = Customer.objects.create_user(
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    CNIC=form.cleaned_data['CNIC'],
                    address=form.cleaned_data['address'],
                    phone=form.cleaned_data['phone'],
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    password2=form.cleaned_data['password2'],
                    profile_image=request.FILES['profile_image']
                )

                # Add profile picture to the storage
                if 'profile_image' in request.FILES:
                    profile_image = request.FILES['profile_image']
                    user.profile_image = profile_image

                    fs = FileSystemStorage()
                    filename = fs.save(user.profile_image.name, user.profile_image)
                    user.profile_image = fs.url(filename)
                    user.save()
                else:
                    print("\n*******************else block \n")
                    user.profile_image = './static/assets/profile_img/default.jpg'

                # generate a unique verification token
                token = str(uuid.uuid4())
                # store the token in the user's profile
                user.auth_token = token
                user.save()
                # send the verification email
                verification_link = request.build_absolute_uri(reverse('verify_customer', kwargs={'auth_token':token}))
                send_mail(
                    'Verify your email address',
                    f'Please click the link to verify your email address: {verification_link}',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return redirect('token_send')
    else:
        form = CustomerSignupForm()
        return render(request, 'customer_register.html', {'form': form})


def customer_login(request):
    form = CustomerLoginForm(request.POST or None)
    if form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect("customer_dashboard")
    return render(request, "customer_login.html", {"form": form})


def customer_logout(request):
    logout(request)
    return redirect("home")



def tailor_signup_view(request):
    if request.method == 'POST':
        form = TailorSignupForm(request.POST)
        if form.is_valid():
            # form.clean_cpassword2()
            form.save()
            return redirect('home')
    else:
        form = TailorSignupForm()
    return render(request, 'signup.html', {'form': form})

def tailor_login(request):
    form = TailorLoginForm(request.POST or None)
    if form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect("tailor_dashboard")
    return render(request, "tailor_login.html", {"form": form})


def tailor_logout(request):
    logout(request)
    return redirect("home")