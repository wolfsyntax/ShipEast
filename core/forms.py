from django import forms
from django.contrib.auth.models import User
from auth0.models import Profile, Detail
from django.conf import settings
#from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
#from django.template.loader import get_template, render_to_string
from django.http import HttpResponse, HttpResponseRedirect

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

class UserEditForm(forms.Form):

    email = forms.CharField(max_length=254, error_messages={'required':'Email is required.'})
    first_name = forms.CharField(max_length=30, error_messages={'required':'First name is required.'})
    last_name = forms.CharField(max_length=30, error_messages={'required':'Last name is required.'})
    passwd = forms.CharField(max_length=30, error_messages={'required':'New Password is required.'})
    conf_password = forms.CharField(max_length=30, error_messages={'required':'Confirm Password is required.'})
    trn = forms.CharField(max_length=9, error_messages={'required':'TRN is required.'})
    address = forms.CharField(max_length=30, error_messages={'required':'Address is required.'})
    parish = forms.ChoiceField(choices=PARISH, error_messages={'required':'Parish is required.'})
    is_agree = forms.BooleanField(error_messages={'required':'You must accept the Term of Use and Policy.'})
    phone = forms.CharField(max_length=10, error_messages={'required':'Mobile number is required.'})

    def clean(self):
        cd = super(UserEditForm, self).clean()
        return cd

    def clean_email(self):
        # Get the email
        email = self.cleaned_data.get('email', '')

        # Check to see if any users already exist with this email as a username.
        try:
            print("\n\nEmail (self) \n{}\n\n".format(email))
            match = User.objects.get(email=email)

        except User.DoesNotExist:
            # Unable to find a user, this is fine
            return email
        return email
        # A user was found with this as a username, raise an error.
        #raise forms.ValidationError('This Email address is already in use.')

    def clean_passwd(self):

        password = self.cleaned_data.get("passwd","")
        #        print("\n\nDEBUG (forms: clean_passwd): {}\n".format(self.cleaned_data))
        if not re.match('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$', password):
            raise forms.ValidationError('New Password must contains alpha-numeric and special characters.')
        return password

    def clean_conf_password(self):
        """Check if both password matches"""
        cd = self.cleaned_data
        print("\n\nDEBUG (forms: clean_conf_password): {}\n".format(cd))
        return HttpResponse(cd)
        if cd['passwd'] != cd['conf_password']:
            raise forms.ValidationError("Passwords don't match.")

        return cd['conf_password']

    def save(self):
        cd = self.cleaned_data
        return True

#class ProfileEditForm(forms.Form):

#    def clean(self):
#        cd = super(ProfileEditForm, self).clean()
#        return cd
