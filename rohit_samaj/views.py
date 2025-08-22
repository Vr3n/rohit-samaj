from django.contrib import messages
from django.http import (HttpRequest, HttpResponse,
                         HttpResponsePermanentRedirect)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')