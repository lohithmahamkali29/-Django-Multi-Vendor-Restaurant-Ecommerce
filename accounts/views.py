from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User, userProfile
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from vendor.forms import VendorForm
from .utils import detectUser,send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.exceptions import PermissionDenied

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.shortcuts import redirect
from accounts.models import User  # Make sure your custom User model is imported



#restrict the vendor from accessign the customer page
from django.core.exceptions import PermissionDenied as permissionDenied

# restrict the vendor from accessing the customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise permissionDenied

# restrict the customer from accessing the vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise permissionDenied
# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Create the user using the form
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            # Create the user using create_user method
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered sucessfully!')
            return redirect('registerUser')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('registerVendor')
    elif request.method == 'POST':
        # store the data and create the user
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()
            vendor = v_form.save(commit=False)
            vendor.user = user
            vendor_name = v_form.cleaned_data['vendor_name']
            user_profile = userProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
   

             mail_subject = 'Please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Your account has been registered sucessfully! Please wait for the approval.')
            return redirect('registerVendor')
        else:
            print('invalid form')
            print(form.errors)
    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'form': form,
        'v_form': v_form,
    }

    return render(request, 'accounts/registerVendor.html', context)
def activate(request, uidb64, token):
    try:
        # Decode the base64 UID to get the user ID
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account has been activated.')
        return redirect('myAccount')  # Make sure 'login' is the name of your login URL pattern
    else:
        messages.error(request, 'Activation link is invalid or has expired.')
        return redirect('myAccount')  # Make sure this is the name of your registration URL pattern

def login(request):
    if request.user.is_authenticated:  # ✅ Fix here
        messages.warning(request, 'You are already logged in!')
        return redirect('myAccount')

    elif request.method == 'POST':  
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('myAccount')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth_logout(request)
    messages.success(request, 'You are now logged out.')
    return redirect('login')



@login_required(login_url = "login")
def myAccount(request):
    user = request.user
    redirect_url = detectUser(user)
    return redirect(redirect_url)
    return render(request, 'accounts/myaccount.html')

@login_required(login_url = "login")
@user_passes_test(check_role_customer)
def CustDashboard(request):
    return render(request,'accounts/custDashboard.html')

@login_required(login_url = "login")
@user_passes_test(check_role_vendor)
def VendorDashboard(request):
    return render(request,'accounts/vendorDashboard.html')

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        if User.objects.filter(email=email).exists():
            user =User.objects.get(email__exact=email)

            #send reset password email
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/emails/forgotPassword.html')
def resetpassword_validate(request, uidb64, token):
    return render(request, 'accounts/resetPassword.html')
    
def  resetPassword(request):
    return render(request, 'accounts/resetPassword.html')