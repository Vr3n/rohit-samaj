from django.contrib import messages
from django.http import HttpRequest, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.urls import reverse

from survey.forms import AcceptTermsForm


def index(request):
    return render(request, 'index.html')


def accept_terms(request: HttpRequest):
    if request.method == "POST":
        form = AcceptTermsForm(request.POST)
        if form.is_valid():
            return HttpResponsePermanentRedirect(reverse('survey:survey_form'))
        else:
            messages.error("Please accept the terms and conditions.")

    return HttpResponsePermanentRedirect(reverse('index'))
