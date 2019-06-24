from django.shortcuts import render, HttpResponse, HttpResponseRedirect

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login")
def index(request):
#    return HttpResponse("Inventory Index")
    context = {
        'main' : 'inventory'
    }

    return render(request, "inventory/index.html",context)