from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from user.models import Customer

@login_required
def customer_dashboard(request):
    user = request.user
    customer_profile = get_object_or_404(Customer, username=user.username)
    # jcustomer_id = customer_profile.jcustomer_id
    username = customer_profile.username
    address = customer_profile.address
    email = customer_profile.email
    # physical_shop_address = customer_profile.t_physical_shop_address
    CNIC = customer_profile.CNIC
    first_name = customer_profile.first_name
    last_name = customer_profile.last_name
    phone = customer_profile.phone
    profile_image = customer_profile.profile_image
    # ...and so on
    context = {
        'name': username,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'address': address,
        'email': email,
        'CNIC': CNIC,
        'profile_image': profile_image

    }

    print(context)
    # jcustomer = Customer.objects.filter(username=request.user.username).first()
    # print(jcustomer.username)
    # print(jcustomer.password)
    # print(jcustomer.email)
    return render(request, 'customer_dashboard/customerdashboard.html', context)


@login_required
def view_customer_profile(request):
    user = request.user
    customer_profile = get_object_or_404(Customer, username=user.username)
    # jcustomer_id = customer_profile.jcustomer_id
    username = customer_profile.username
    address = customer_profile.address
    email = customer_profile.email
    # physical_shop_address = customer_profile.t_physical_shop_address
    CNIC = customer_profile.CNIC
    first_name = customer_profile.first_name
    last_name = customer_profile.last_name
    phone = customer_profile.phone
    profile_image = customer_profile.profile_image


    context = {
        'name': username,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'address': address,
        'email': email,
        'CNIC': CNIC,
        'profile_image': profile_image

    }

    print(context)

    return render(request, 'home.html', context)

@login_required
def c_accountinfo(request):
    user = request.user
    customer_profile = get_object_or_404(Customer, username=user.username)
    # jcustomer_id = customer_profile.jcustomer_id
    username = customer_profile.username
    address = customer_profile.address
    email = customer_profile.email
    # physical_shop_address = customer_profile.t_physical_shop_address
    CNIC = customer_profile.CNIC
    first_name = customer_profile.first_name
    last_name = customer_profile.last_name
    phone = customer_profile.phone
    profile_image = customer_profile.profile_image
    # ...and so on
    context = {
        'name': username,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'address': address,
        'email': email,
        'CNIC': CNIC,
        'profile_image': profile_image


    }

    print(context)
    return render(request, 'customer_dashboard/c_accountinfo.html', context=context)

@login_required
def c_totalorders(request):
    return render(request, 'customer_dashboard/myorders.html')
