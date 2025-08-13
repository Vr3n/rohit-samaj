from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required

from survey.forms import SamajSurveyForm
from survey.models import (
    Country, District, SamajMember, SamajMemberAddress, SamajMemberEducationalQualification, SamajMemberEmail, SamajMemberIncome, SamajMemberMobileNumber, SamajMemberOccupation, State, Taluka
)

# Create your views here.

@login_required
def profile_completion(request: HttpRequest):
    context = {}
    samaj_member = SamajMember.objects.filter(user=request.user).first()
    
    profile_sections = {
        "Membership": False,
        "Mobile Number": False,
        "Email": False,
        "Home Address": False,
        "Educational Qualification": False,
        "Occupation": False,
        "Income": False,
    }

    if samaj_member:
        if SamajMember.objects.filter(user=request.user).exists():
            profile_sections["Membership"] = True
        if SamajMemberMobileNumber.objects.filter(member=samaj_member).exists():
            profile_sections["Mobile Number"] = True
        if SamajMemberEmail.objects.filter(member=samaj_member).exists():
            profile_sections["Email"] = True
        if SamajMemberAddress.objects.filter(member=samaj_member).exists():
            profile_sections["Home Address"] = True
        if SamajMemberEducationalQualification.objects.filter(member=samaj_member).exists():
            profile_sections["Educational Qualification"] = True
        if SamajMemberOccupation.objects.filter(member=samaj_member).exists():
            profile_sections["Occupation"] = True
        if SamajMemberIncome.objects.filter(member=samaj_member).exists():
            profile_sections["Income"] = True

    completed_fields = sum(profile_sections.values())
    total_fields = len(profile_sections)
    profile_completion_percentage = (completed_fields / total_fields) * 100

    context['profile_completion_percentage'] = profile_completion_percentage
    context['profile_sections'] = profile_sections
    context['profile_incomplete'] = completed_fields < total_fields

    return render(request, "survey/partials/_profile_completion.html", context)

def survey_sucess(request: HttpRequest):
    return render(request, 'survey/survey_success.html')


def samaj_survey(request: HttpRequest):
    context = {}
    if request.method == "POST":
        form = SamajSurveyForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    form.save()
                    messages.success(request, "Survey Completed Successfully!")
                    return redirect(reverse('survey:survey_sucess'))
            except Exception as e:
                print("There was an unexpected error.", str(e))
                messages.error(
                    request, "Your form has errors please fix them.")
        else:
            messages.error(
                request, "Your form has errors please fix them.", form.errors)
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


def check_mobile_exists(request: HttpRequest) -> JsonResponse:
    mobile_no = request.GET.get("mobile_number")

    is_exist = SamajMemberMobileNumber.objects.filter(
        mobile_number=mobile_no
    ).exists()

    print(is_exist)

    return JsonResponse({ 'exists': is_exist })

