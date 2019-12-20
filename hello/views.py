import logging

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Greeting
from .auth import authenticate_github_webhook_request

logger = logging.getLogger(__name__)

def index(request):
    return render(request, "index.html")

import functools

def requires_github_hmac(view_func):

    @functools.wraps(view_func)
    def wrapper(request):
        authenticate_github_webhook_request(request)
        return view_func(request)

    return wrapper


@csrf_exempt
@requires_github_hmac
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
