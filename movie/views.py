from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    #return HttpResponse("<h1>Welcome to the Movie Reviews Home Page!<h1>")
    #return render(request, 'home.html')
    return render(request, 'home.html', {'name': 'Jerónimo Restrepo Cardona'})

def about(request):
    return HttpResponse("<h1>About Movie Reviews Page</h1>")
