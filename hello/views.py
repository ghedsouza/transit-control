import logging

from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")

def github(request):
    if request.POST:
        logger.warning(f"xxx github POST: {request.POST}.")
    else:
        logger.warning(f"xxx github GET: {request.build_absolute_uri()}.")
    return HttpResponse('Hello.')

def ping(request):
    logger.error(f'Error: {request}.')
    logger.debug(f'Debug: {request}.')
    logger.info(f'Info: {request}.')
    logger.warning(f'Warning: {request}.')
    if request.POST:
        print(f"xxx POST: {request.POST}.")
    else:
        print(f"xxx GET: {request.build_absolute_uri()}.")
    return HttpResponse(';)')

def db(request):
    greeting = Greeting()
    greeting.save()
    greetings = Greeting.objects.all()
    return render(request, "db.html", {"greetings": greetings})
