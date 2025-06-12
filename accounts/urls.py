# accounts/urls.py

from django.urls import path
from . import views


urlpatterns = [
    path('registerUser/', views.registerUser, name='registerUser'),
    path('registerVendor/', views.registerVendor, name='registerVendor'),

    path('login/', views.login, name='login'),
    path('logout/',views.logout,name='logout'),
    path('myAccount/',views.myAccount,name='myAccount'),
    path('custDashboard/',views.CustDashboard,name='custDashboard'),
    path('vendorDashboard/',views.VendorDashboard,name='vendorDashboard'),
]

