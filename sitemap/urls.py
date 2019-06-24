from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
	url(r'^$',views.home, name='home'),
	url(r'^about$',views.about, name='about'),
	url(r'^contact$',views.contact, name='contact'),
	url(r'^how-it-works$',views.contact, name='how_it_works'),
	url(r'^service$',views.service, name='service'),

]