from django.contrib import messages
from django.http import (HttpRequest, HttpResponse,
                         HttpResponsePermanentRedirect)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from survey.forms import AcceptTermsForm


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return render(request, 'index.html')


def accept_terms(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = AcceptTermsForm(request.POST)
        if form.is_valid():
            return HttpResponsePermanentRedirect(reverse('survey:survey_form'))
        else:
            messages.error(
                request,
                "Please accept the terms and conditions.")

    return HttpResponsePermanentRedirect(reverse('index'))
