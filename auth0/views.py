from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from auth0.forms import LoginForm, UserRegistrationForm, UserEditForm #, ProfileEditForm

from .models import Profile, Detail
from django.contrib.auth.models import User

from django.contrib import messages
from django.template.loader import get_template
from django.template import Context

from django.conf import settings
#from smtplib import SMTP_SSL as SMTP
#from email.mime.text import MIMEText

from django.conf import settings
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string

def user_login(request):
#    return HttpResponse("LOGIN")
    if request.user.is_authenticated :
        return HttpResponseRedirect("/dashboard")
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        #print("\n\n\n\nDEBUG user_login (fn)\n\n\n\n")
        if form.is_valid():
            print("\n\n\n\nDEBUG form valid\n\n\n\n")
            cd = form.cleaned_data
            username = cd['email'].split("@")[0]
            user = authenticate(username=username, password=cd['password'])
            #print("\n\nDEBUG username: {}\n\n".format(username))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    #request.session["userData"] = request.user
                    #return HttpResponse('Authenticated successfully')
                    return HttpResponseRedirect("/dashboard")
                else:
                    #return HttpResponse('Disabled account')
                    messages.add_message(request, messages.INFO, "Account is not 'active'. Please contact your Administrator.")
            else:
                #return HttpResponse('Invalid login')
                messages.add_message(request, messages.WARNING, "Invalid Username or Password.")
    else:
        
        form = LoginForm()
    
#    return render(request, 'registration/login.html', {'form': form})
    return render(request, 'login.html', {'form': form})

#    else:
#



def register(request):

    if request.user.is_authenticated :
        return HttpResponseRedirect("/dashboard")

    if request.method == 'POST':

        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form
            # Set the chosen password
#            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()


            # Create the user profile
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

@login_required(login_url="/login")
def account_settings(request):

    user_id = request.user.id
    
    context = {
        "user_info" : User.objects.get(id=user_id),
        "personal_detail" : Detail.objects.get(user_id=user_id)
    }

    if request.method == 'POST':
        #print("\n\n\n\nSubmitted Data: {}\n\n".format(request.POST))
        new_form = UserEditForm(request.POST)
        
        #print("\n\nNew Form (POST): \n{}\n\n{}\n\n\n\n".format(new_form.clean,request.user.id))

        if new_form.is_valid():
            #return HttpResponse("Form is Valid")
            new_form.save()
            return HttpResponseRedirect("/dashboard")
        #else:
        #    return HttpResponse("Invalid Form") #Redirect("/account/settings")
        #else:
        #    return HttpResponse("Form is not Valid")

    else:

        new_form = UserEditForm()

    context.setdefault('form', new_form)

    return render(request,"account/settings.html",context)

#@login_required
#def edit(request):
#    if request.method == 'POST':
#        user_form = UserEditForm(instance=request.user,
#                                 data=request.POST)
#        profile_form = ProfileEditForm(instance=request.user.profile,
#                                       data=request.POST,
#                                       files=request.FILES)
#        if user_form.is_valid() and profile_form.is_valid():
#            user_form.save()
#            profile_form.save()
#            messages.success(request, 'Profile updated successfully')
#        else:
#            messages.error(request, 'Error updating your profile')
#    else:
#        user_form = UserEditForm(instance=request.user)
#        profile_form = ProfileEditForm(instance=request.user.profile)
#    return render(request, 'account/edit.html', {'user_form': user_form,
#                                                 'profile_form': profile_form})



@login_required(login_url='/login')
def dashboard(request):
#    return HttpResponse("Hello")
#    return HttpResponse("DASHBOARD")
    context = {
        'section': 'dashboard',
        'main': 'home',
        'detail' : Detail.objects.get(user_id=request.user.id),
    }

    return render(request, 'account/dashboard.html', context)

def emailer(request):
    subject = '(Test) Registration Info'

    message = get_template('email_template.html').render(
        {
            'first_name': 'Jayson',
            'last_name': 'Alpe',
            'phone': '+63918-459-2272',
            'parish': 'St. Dominic',
            'trn': '87000',
            'address': 'Camarines Sur'
        }
    )

    email_from = settings.EMAIL_HOST_USER

#    email = EmailMultiAlternatives(subject, "Hello, World!", to=["airdrop.crazywolf@gmail.com", ], bcc=['mail.goats@gmail.com', ], reply_to=['jaysonalpe@gmail.com'])
    email = EmailMultiAlternatives(subject,message, to=["airdrop.crazywolf@gmail.com", ], reply_to=['jaysonalpe@gmail.com'])
    email.content_subtype = "html"
    email.attach_alternative(message, "text/html")
    email.send()
#    send_mail(subject + " sent using send_mail", message, email_from, ['delatrinidadjoseph@gmail.com', ], html_message=message)
    return HttpResponse("Email sent to {} !".format(email_from))
