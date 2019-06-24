from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import logout_then_login
from django.contrib.auth import views as auth_views

urlpatterns = [

    url(r'^email/me$',views.emailer, name='send_mail'),
    #url(r'^edit/$', views.edit, name='edit'),
    url(r'^account/settings$', views.account_settings, name='account-setting'),
    url(r'^register/$', views.register, name='register'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    # login / logout urls
    url(r'^login/$', views.user_login, name="login"),
    #url(r'^login$', LoginView.as_view(template_name='registration/login.html'), name="login"),
    url(r'^logout/$', LogoutView.as_view(template_name='registration/logged_out.html'), name="logout"),
    url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    # passwords change
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    # password restore
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #path('register/', auth_views.register, name='register'),
    #path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='password_reset'),
    path('password-reset-confirm/ <uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),

]

