from django.shortcuts import render
from django.http import HttpResponse  # ✅ Needed for HttpResponse

# Create your views here.
def registerUser(request):
    return render(request,'accounts/registerUser.html')
