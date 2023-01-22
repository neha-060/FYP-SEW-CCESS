from django.urls import path, include
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static
from tailor.views import tailor_dashboard, t_accountinfo, totalorders, add_service, services
from customer.views import customer_dashboard, c_accountinfo, c_totalorders

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('admin', admin.site.urls),
    path('', views.home, name= 'home'),
    path('login_page', views.login_page, name= 'login_page'),
    path('signup_page', views.signup_page, name= 'signup_page'),
    path('tailor_register', views.tailor_register, name= 'tailor_register'),
    path('tailor_login', views.tailor_login, name= 'tailor_login'),
    path('tailor_logout', views.tailor_logout, name= 'tailor_logout'),
    path('customer_register', views.customer_register, name= 'customer_register'),
    path('customer_login', views.customer_login, name= 'customer_login'),
    path('customer_logout', views.customer_logout, name= 'customer_logout'),
    path('termsandconditions', views.termsandconditions, name= 'termsandconditions'),
    path('tailor_dashboard', tailor_dashboard, name= 'tailor_dashboard'),
    path('t_accountinfo', t_accountinfo, name= 't_accountinfo'),
    path('totalorders', totalorders, name= 'totalorders'),
    path('customer_dashboard', customer_dashboard, name= 'customer_dashboard'),
    path('c_accountinfo', c_accountinfo, name= 'c_accountinfo'),
    path('c_totalorders', c_totalorders, name= 'c_totalorders'),
    path('findopportunities', views.findopportunities, name= 'findopportunities'),
    path('findtailor', views.findtailor, name= 'findtailor'),
    path('token_send', views.token_send, name= 'token_send'),
    path('success', views.success, name= 'success'),
    path('success', views.success, name= 'success'),
    path('verify_customer/<str:auth_token>/', views.verify_customer, name='verify_customer'),
    path('verify_tailor/<str:auth_token>/', views.verify_tailor, name='verify_tailor'),
    path('services', services, name='services'),
    path('add_service', add_service, name= 'add_service'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)