from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpRequest
from django.urls import reverse

from survey.forms import SamajSurveyForm
from survey.models import (
    Country, District, State, Taluka
)

# Create your views here.


def survey_sucess(request: HttpRequest):
    return render(request, 'survey/survey_success.html')


def samaj_survey(request: HttpRequest):
    context = {}
    if request.method == "POST":
        form = SamajSurveyForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Survey Completed Successfully!")
            return redirect(reverse('survey:survey_sucess'))
        else:
            messages.error(request, "Your form has errors please fix them.")
    else:
        form = SamajSurveyForm()
        context['countries'] = Country.objects.all()

        # By default india is selected.
        context['states'] = State.objects.filter(country_id=1)

    context['form'] = form

    return render(request, 'survey/form.html', context=context)


def hx_perm_district_select(request: HttpRequest):
    context = {}
    state_id = request.GET.get('perm_state')

    try:
        state_id = int(state_id)
    except ValueError:
        state_id = None

    if state_id:
        context['districts'] = District.objects.filter(
            state_id=state_id).order_by('name')

    return render(request, "survey/hx/perm_district_select.html", context)


def hx_corr_district_select(request: HttpRequest):
    context = {}
    state_id = request.GET.get('corr_state')

    try:
        state_id = int(state_id)
    except ValueError:
        state_id = None

    if state_id:
        context['districts'] = District.objects.filter(
            state_id=state_id).order_by('name')

    return render(request, "survey/hx/corr_district_select.html", context)


def hx_corr_taluka_select(request: HttpRequest):
    context = {}
    district_id = request.GET.get('corr_district')

    try:
        district_id = int(district_id)
    except ValueError:
        district_id = None

    if district_id:
        context['talukas'] = Taluka.objects.filter(
            district_id=district_id).order_by('name')

    return render(request, "survey/hx/corr_taluka_select.html", context)


def hx_perm_taluka_select(request: HttpRequest):
    context = {}
    district_id = request.GET.get('perm_district')

    try:
        district_id = int(district_id)
    except ValueError:
        district_id = None

    if district_id:
        context['talukas'] = Taluka.objects.filter(
            district_id=district_id).order_by('name')

    return render(request, "survey/hx/perm_taluka_select.html", context)
