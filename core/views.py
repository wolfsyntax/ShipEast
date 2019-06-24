from django.shortcuts import render, HttpResponse
import datetime

# Create your views here.
from payoneer.utils import render_to_pdf #created in step 4
from django.views.generic import View

def index(request):
    return HttpResponse("Invoice Index")

def show(request):
    return HttpResponse("Show Invoice")

def print_pdf(request):
    #return HttpResponse("Printing PDF")
    data = {
        'company_name': 'Ship East',
        'tax_id': '00190313600001',
        'company_address': '5-7 ROOSEVELT AVE, SUITE A, KINGSTON 6, JAMAICA 5',
        'company_tel': '(876) 619-7447',
        'today': str(datetime.date.today()),
        'amount': str(39.99),
        'customer_name': 'Cooper Mann',
        'order_id': str(1233434),
    }

    pdf = render_to_pdf('pdf/invoice.html', data)
    return HttpResponse(pdf, content_type='application/pdf')


class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        data = {
            'company_name:' : 'Ship East',
            'tax_id' : '00190313600001',
            'company_address' : '5-7 ROOSEVELT AVE, SUITE A, KINGSTON 6, JAMAICA 5',
            'company_tel' : '(876) 619-7447',
             'today': datetime.date.today(),
             'amount': 39.99,
            'customer_name': 'Cooper Mann',
            'order_id': 1233434,
        }
        pdf = render_to_pdf('pdf/invoice.html', data)
        return HttpResponse(pdf, content_type='application/pdf')