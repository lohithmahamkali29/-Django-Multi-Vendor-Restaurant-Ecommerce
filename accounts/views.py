from django.shortcuts import render ,redirect
from django.http import HttpResponse  # ✅ Needed for HttpResponse
from .forms import UserForm  # ✅ Needed for UserForm
from .models import User  # ✅ Needed for User model
from django.contrib import messages
# Create your views here.
def registerUser(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # form.clean()  
            password = form.cleaned_data['password']
            user = form.save(commit=False)
            user.set_password(password)
            user.role = User.CUSTOMER
            user.save()  # Don't forget to save the user instance
            messages.success(request, 'User registered successfully. You can now log in.'  )
            return redirect('registerUser')
        else:
            print('Invalid form')
            print(form.errors)
    else:
        form = UserForm()
    
    context = {
        'form': form,
    }
    return render(request, 'accounts/registerUser.html', context)
