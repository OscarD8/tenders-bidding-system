from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'pages/index.html')

def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return HttpResponse("Contact Page")