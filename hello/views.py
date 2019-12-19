from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")


def ping(request):
    if request.POST:
        print(f"xxx POST: {request.POST}.")
    else:
        print(f"xxx GET: {request.build_absolute_uri()}.")
    return HttpResponse('pong')

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})
