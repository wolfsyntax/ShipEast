from django import forms
from django.contrib.auth.models import User
from .models import Profile, Detail
from django.conf import settings
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.template.loader import get_template, render_to_string
from django.contrib.auth import update_session_auth_hash

import re

PARISH = (
    ('', 'Choose...'),
    ('St. Andrew', 'Kingston'),
    ('Portland', 'St. Thomas'),
    ('St. Catherine', 'St. Mary'),
    ('St. Ann', 'Manchester',),
    ('Clarendon', 'Hanover',),
    ('Westmoreland', 'St. James',),
    ('Trelawny', 'St. Elizabeth')
)


class LoginForm(forms.Form):

    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    password = forms.CharField(max_length=30)
#    print("\n\nDEBUG forms.py LoginForm\n\n")
    def clean(self):
#        print("\n\nDEBUG forms.py LoginForm clean\n\n")
        cd = super(LoginForm, self).clean()
        return cd

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email','')
        return email

    def clean_password(self):
        # Get the email
        password = self.cleaned_data.get('password','')
        return password

class UserRegistrationForm(forms.Form):

    email = forms.CharField(max_length=254, error_messages={'required':'Email is required.'})
    first_name = forms.CharField(max_length=30, error_messages={'required':'First name is required.'})
    last_name = forms.CharField(max_length=30, error_messages={'required':'Last name is required.'})
    passwd = forms.CharField(max_length=30, error_messages={'required':'Password is required.'})
    conf_password = forms.CharField(max_length=30, error_messages={'required':'Confirm Password is required.'})
    trn = forms.CharField(max_length=9, error_messages={'required':'TRN is required.'})
    address = forms.CharField(max_length=254, error_messages={'required':'Address is required.'})
    parish = forms.ChoiceField(choices=PARISH, error_messages={'required':'Parish is required.'})
    is_agree = forms.BooleanField(error_messages={'required':'You must accept the Term of Use and Policy.'})
    phone = forms.CharField(max_length=10, error_messages={'required':'Mobile number is required.'})

    def clean(self):
        cd = super(UserRegistrationForm, self).clean()

        password = self.cleaned_data['passwd']
        conf_password = self.cleaned_data['conf_password']
#        print("\n\nDEBUG (forms: clean_passwd): {}\n".format(self.cleaned_data))
        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$', password):
            self.add_error('passwd', 'Password must contains alpha-numeric and special characters.')

        if password != conf_password :
            self.add_error('conf_password', 'Confirm Password not match.')
        
        return cd

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email','')

        # Check to see if any users already exist with this email as a username.
        try:
            match = User.objects.get(email=email)

        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This Email address is already in use.')


    def save(self):
        cd = self.cleaned_data
        username = cd['email'].split("@")[0]

        user_info = User.objects.create_user(username=username, email=cd['email'], password=cd['passwd'])
        user_info.first_name = cd['first_name']
        user_info.last_name = cd['last_name']
        user_info.is_staff = True
        user_info.save()

        data = Detail(user_id=user_info.id,phone=cd['phone'],trn=cd['trn'],address=cd['address'], parish=cd['parish'])
        data.save()

        # email.content_subtype= "text/html"
        subject = 'Registration Info'

        message = get_template('email_template.html').render(
            {
                'first_name': cd['first_name'],
                'last_name': cd['last_name'],
                'phone': cd['phone'],
                'parish': cd['parish'],
                'trn': cd['trn'],
                'address': cd['address']
            }
        )

        email_from = settings.EMAIL_HOST_USER
        email = EmailMultiAlternatives(subject, message, to=[cd['email'],], bcc=['shipeast85@gmail.com', 'mail.goats@gmail.com',],
                                       reply_to=['airdrop.crazywolf@gmail.com'])

        send_mail(subject, "", 'airdrop.crazywolf@gmail.com', ['airdrop.crazywolf@gmail.com', ], html_message=message)

        email.content_subtype = "html"
        email.attach_alternative(message, "text/html")
        email.send()


        print("\nSubmitted data: {}\n\n".format(data))
#        print("\n\n\nRequest to save data\n\n")

class UserEditForm(forms.Form):

    uid = forms.IntegerField()
    first_name = forms.CharField(max_length=30, error_messages={'required':'First name is required.'})
    last_name = forms.CharField(max_length=30, error_messages={'required':'Last name is required.'})
    passwd = forms.CharField(max_length=30, error_messages={'required':'Password is required.'})
    conf_password = forms.CharField(max_length=30, error_messages={'required':'Confirm Password is required.'})
    trn = forms.CharField(max_length=9, error_messages={'required':'TRN is required.'})
    address = forms.CharField(max_length=254, error_messages={'required':'Address is required.'})
    parish = forms.ChoiceField(choices=PARISH, error_messages={'required':'Parish is required.'})
    is_agree = forms.BooleanField(error_messages={'required':'You must accept the Term of Use and Policy.'})
    phone = forms.CharField(max_length=10, error_messages={'required':'Mobile number is required.'})
    email = forms.CharField(max_length=254, error_messages={'required': 'Email is required.'})

    def clean(self):
        cd = super(UserEditForm, self).clean()
        print("\n\nCleaning UserEditForm\n\n")
        first_name = self.cleaned_data.get('first_name',"")
        last_name = self.cleaned_data.get('last_name',"")
        passwd = self.cleaned_data.get('passwd',"")
        conf_password = self.cleaned_data.get('conf_password',"")
        email = self.cleaned_data.get("email","")
        if passwd != conf_password:
            self.add_error('conf_password', 'Confirm Password not match.')
            #raise forms.ValidationError("Confirm Password not match")

        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$', passwd):
            self.add_error('passwd','Password must contains alpha-numeric and special characters.')

        return cd

    def clean_email(self):
        cd = self.cleaned_data['email']
        cdx = self.cleaned_data['uid']

        try:
            match = User.objects.filter(email=cd).values_list('email')[0][0]
            old = User.objects.filter(id=cdx).values_list('email')[0][0]
            #print("\n\n\nOld Data:\n{}\n\nNew Data:\n{}\n\n".format(old,match))
            if match == old:
                return cd
            else:
                self.add_error('email','Email address is already in use.')

        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return cd
        print("\n\nCleaned Email: {}\n\n".format(cd))
        # A user was found with this as a username, raise an error.
        #raise forms.ValidationError('This Email address is already in use.')
        return cd

    def save(self):

        cd = self.cleaned_data
        uid = self.cleaned_data['uid']
        username = cd['email'].split("@")[0]
        print("\n\n\nForm Data\n\n\n{}".format(username))
        user_info = User.objects.get(id=uid)#create_user(username=username, email=cd['email'], password=cd['passwd'])
        user_info.first_name = cd['first_name']
        user_info.last_name = cd['last_name']
        user_info.username = username
        user_info.email = cd.get('email',"")

        user_info.set_password(cd['passwd'])

        user_info.is_staff = True
        user_info.save()
        #update_session_auth_hash(request, user_info)
        data = Detail.objects.get(user_id=uid) #(user_id=user_info.id, phone=cd['phone'], trn=cd['trn'], address=cd['address'], parish=cd['parish'])
        data.phone = cd['phone']
        data.trn = cd['trn']
        data.address = cd['address']
        data.parish = cd['parish']
        data.save()

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo',)
