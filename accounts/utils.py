from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
import django
from django.conf import settings
def detectUser(User):
    if User.role == 1:
        redirect_url = 'vendorDashboard'
        return redirect_url
    elif User.role == 2:
       redirect_url = 'custDashboard'
       return redirect_url
    
    elif User.role == None and User.is_superadmin:

        redirect_url = '/admin'
        return redirect_url  
    
def send_verification_email(request, user, mail_subject, email_template):
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(email_template, {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.content_subtype = "html"
    mail.send()