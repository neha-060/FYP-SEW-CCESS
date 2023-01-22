from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from user.models import Tailor, Service
from user.forms import ServiceForm
from django.shortcuts import render, redirect



@login_required
def tailor_dashboard(request):
    user = request.user
    tailor_profile = get_object_or_404(Tailor, username=user.username)
    # tailor_id = tailor_profile.tailor_id
    username = tailor_profile.username
    address = tailor_profile.address
    email = tailor_profile.email
    physical_shop_address = tailor_profile.t_physical_shop_address
    CNIC = tailor_profile.CNIC
    first_name = tailor_profile.first_name
    last_name = tailor_profile.last_name
    phone = tailor_profile.phone
    profile_image = tailor_profile.profile_image
    # ...and so on
    context = {
        'name': username,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'address': address,
        'email': email,
        'physical_shop_address': physical_shop_address,
        'CNIC': CNIC,

    }

    print(context)
    # tailor = Tailor.objects.filter(username=request.user.username).first()
    # print(tailor.username)
    # print(tailor.password)
    # print(tailor.email)
    return render(request, 'tailor_dashboard/tailordashboard.html', context)


@login_required
def view_tailor_profile(request):
    user = request.user
    tailor_profile = get_object_or_404(Tailor, username=user.username)
    # tailor_id = tailor_profile.tailor_id
    username = tailor_profile.username
    address = tailor_profile.address
    email = tailor_profile.email
    physical_shop_address = tailor_profile.t_physical_shop_address
    CNIC = tailor_profile.CNIC
    first_name = tailor_profile.first_name
    last_name = tailor_profile.last_name
    phone = tailor_profile.phone
    profile_image = tailor_profile.profile_image
    # ...and so on
    context = {
        'name': username,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'address': address,
        'email': email,
        'physical_shop_address': physical_shop_address,
        'CNIC': CNIC,
        'profile_image': profile_image

    }

    print(context)


    print(context)
    return render(request, 'home.html', context)

@login_required
def t_accountinfo(request):
    user = request.user
    tailor_profile = get_object_or_404(Tailor, username=user.username)
    # tailor_id = tailor_profile.tailor_id
    username = tailor_profile.username
    address = tailor_profile.address
    email = tailor_profile.email
    physical_shop_address = tailor_profile.t_physical_shop_address
    CNIC = tailor_profile.CNIC
    first_name = tailor_profile.first_name
    last_name = tailor_profile.last_name
    phone = tailor_profile.phone
    profile_image = tailor_profile.profile_image
    # ...and so on
    context = {
        'name': username,
        'first_name': first_name,
        'last_name': last_name,
        'phone': phone,
        'address': address,
        'email': email,
        'physical_shop_address': physical_shop_address,
        'CNIC': CNIC,
        'profile_image': profile_image

    }

    print(context)
    return render(request, 'tailor_dashboard/t_accountinfo.html', context=context)

@login_required
def totalorders(request):
    return render(request, 'tailor_dashboard/totalorders.html')


@login_required
def add_service(request):
    tailor = get_user(request)
    services = Service.objects.filter(tailor=tailor)

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, request=request)

        if form.is_valid():
            #add service image
            service_image = request.FILES['service_image']
            services.service_image = service_image
            fs = FileSystemStorage()
            filename = fs.save(services.service_image.name, services.service_image)
            services.service_image = fs.url(filename)

            #create service
            form.save()
            print("add service")
            return redirect('add_service')
    else:
        form = ServiceForm(request=request)
    return render(request, 'tailor_dashboard/add_service.html', {'form': form, 'services': services})

@login_required
def services(request):
    tailor = get_user(request)
    services = Service.objects.filter(tailor=tailor)
    return render(request, 'tailor_dashboard/services.html', {'services': services})

def edit_service(request, pk):
    service = Service.objects.get(pk=pk)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('services')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'edit_service.html', {'form': form})

def delete_service(request, pk):
    Service.objects.get(pk=pk).delete()
    return redirect('services')