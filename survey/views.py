from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpRequest

from survey.forms import SamajSurveyForm
from survey.models import (
    Country, District, State
)

# Create your views here.


def survey_sucess(request: HttpRequest):
    return render(request, 'survey_success.html')


def samaj_survey(request: HttpRequest):
    context = {}
    if request.method == "POST":
        form = SamajSurveyForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Survey Completed Successfully!")
            return redirect('success_page')
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

    if state_id:
        context['districts'] = District.objects.filter(state_id=state_id)

    return render(request, "survey/hx/perm_district_select.html", context)


def hx_corr_district_select(request: HttpRequest):
    context = {}
    state_id = request.GET.get('corr_state')

    if state_id:
        context['districts'] = District.objects.filter(state_id=state_id)

    return render(request, "survey/hx/corr_district_select.html", context)
