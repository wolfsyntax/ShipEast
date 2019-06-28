from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^$',views.index, name="invoice-list"),
    url(r'^docs/$', views.print_pdf, name="invoice_report"),
    url(r'^view$', views.show, name='invoice_index'),

]