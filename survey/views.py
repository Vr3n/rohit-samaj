from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpRequest, JsonResponse
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from survey.forms import (
    SamajMemberPersonalInfoForm,
    SamajMemberAddressForm,
    SamajMemberEducationalQualificationFormSet,
    SamajMemberOccupationForm,
    SamajMemberIncomeForm,
    AcceptTermsForm,
    text_input_attrs,
)
from survey.models import (
    City,
    Country,
    District,
    SamajMember,
    SamajMemberAddress,
    SamajMemberEducationalQualification,
    SamajMemberEmail,
    SamajMemberIncome,
    SamajMemberMobileNumber,
    SamajMemberOccupation,
    State,
    Taluka,
)


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
        if SamajMemberEducationalQualification.objects.filter(
            member=samaj_member
        ).exists():
            profile_sections["Educational Qualification"] = True
        if SamajMemberOccupation.objects.filter(member=samaj_member).exists():
            profile_sections["Occupation"] = True
        if SamajMemberIncome.objects.filter(member=samaj_member).exists():
            profile_sections["Income"] = True

    completed_fields = sum(profile_sections.values())
    total_fields = len(profile_sections)
    profile_completion_percentage = (completed_fields / total_fields) * 100

    context["profile_completion_percentage"] = profile_completion_percentage
    context["profile_sections"] = profile_sections
    context["profile_incomplete"] = completed_fields < total_fields

    return render(request, "survey/partials/_profile_completion.html", context)


def survey_sucess(request: HttpRequest):
    return render(request, "survey/survey_success.html")


class SamajMemberCreateView(LoginRequiredMixin, View):
    template_name = "survey/personal_info_form.html"

    def get(self, request: HttpRequest, *args, **kwargs):
        form = SamajMemberPersonalInfoForm()
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, *args, **kwargs):
        form = SamajMemberPersonalInfoForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    member = form.save(commit=False)
                    member.added_by = request.user
                    member.save()

                    member.mobile_numbers.all().delete()
                    member.emails.all().delete()

                    if form.cleaned_data.get("mobile_number"):
                        SamajMemberMobileNumber.objects.create(
                            member=member,
                            mobile_number=form.cleaned_data["mobile_number"],
                        )
                    if form.cleaned_data.get("alternate_mobile_number"):
                        SamajMemberMobileNumber.objects.create(
                            member=member,
                            mobile_number=form.cleaned_data["alternate_mobile_number"],
                        )
                    if form.cleaned_data.get("email"):
                        SamajMemberEmail.objects.create(
                            member=member, email=form.cleaned_data["email"]
                        )
                    if form.cleaned_data.get("alternate_email"):
                        SamajMemberEmail.objects.create(
                            member=member, email=form.cleaned_data["alternate_email"]
                        )

                    messages.success(
                        request, "Personal Information Saved Successfully!"
                    )
                    return redirect(
                        reverse("survey:address_form", kwargs={"member_id": member.id})
                    )
            except Exception as e:
                messages.error(request, f"There was an unexpected error: {e}")
        else:
            messages.error(request, "Please correct the errors below.")

        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


class SamajMemberAddressView(LoginRequiredMixin, View):
    template_name = "survey/address_form.html"

    def get(self, request: HttpRequest, member_id: int, *args, **kwargs):
        member = get_object_or_404(SamajMember, id=member_id)
        corr_address = SamajMemberAddress.objects.filter(
            member=member, address_type="Correspondence"
        ).first()
        perm_address = SamajMemberAddress.objects.filter(
            member=member, address_type="Permanent"
        ).first()

        try:
            india = Country.objects.get(name="India")
        except Country.DoesNotExist:
            india = None

        corr_address_form = SamajMemberAddressForm(
            instance=corr_address,
            prefix="corr",
            initial={"country": india.id if india else None},
        )
        perm_address_form = SamajMemberAddressForm(
            instance=perm_address,
            prefix="perm",
            initial={"country": india.id if india else None},
        )

        corr_address_form.fields["country"].queryset = Country.objects.all()
        perm_address_form.fields["country"].queryset = Country.objects.all()

        if india:
            corr_address_form.fields["state"].queryset = State.objects.filter(country=india)
            perm_address_form.fields["state"].queryset = State.objects.filter(country=india)

        context = {
            "member": member,
            "corr_address_form": corr_address_form,
            "perm_address_form": perm_address_form,
            "text_input_attrs": text_input_attrs,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, member_id: int, *args, **kwargs):
        member = get_object_or_404(SamajMember, id=member_id)
        corr_address = SamajMemberAddress.objects.filter(
            member=member, address_type="Correspondence"
        ).first()
        perm_address = SamajMemberAddress.objects.filter(
            member=member, address_type="Permanent"
        ).first()

        corr_address_form = SamajMemberAddressForm(
            request.POST, instance=corr_address, prefix="corr"
        )
        perm_address_form = SamajMemberAddressForm(
            request.POST, instance=perm_address, prefix="perm"
        )

        if corr_address_form.is_valid() and perm_address_form.is_valid():
            try:
                with transaction.atomic():
                    corr_address_instance = corr_address_form.save(commit=False)
                    corr_address_instance.member = member
                    corr_address_instance.address_type = "Correspondence"
                    corr_address_instance.save()

                    if corr_address_form.cleaned_data.get(
                        "is_permanent_same_as_correspondence"
                    ):
                        if perm_address:
                            perm_address.delete()
                        perm_address = corr_address_instance
                        perm_address.pk = None
                        perm_address.address_type = "Permanent"
                        perm_address.save()
                    else:
                        perm_address_instance = perm_address_form.save(commit=False)
                        perm_address_instance.member = member
                        perm_address_instance.address_type = "Permanent"
                        perm_address_instance.save()

                    messages.success(request, "Address Information Saved Successfully!")
                    return redirect(
                        reverse(
                            "survey:education_form", kwargs={"member_id": member.id}
                        )
                    )
            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {e}")
        else:
            messages.error(request, "Please correct the errors below.")

        try:
            india = Country.objects.get(name="India")
        except Country.DoesNotExist:
            india = None
            
        corr_address_form.fields["country"].queryset = Country.objects.all()
        perm_address_form.fields["country"].queryset = Country.objects.all()

        if india:
            corr_address_form.fields["state"].queryset = State.objects.filter(country=india)
            perm_address_form.fields["state"].queryset = State.objects.filter(country=india)

        context = {
            "member": member,
            "corr_address_form": corr_address_form,
            "perm_address_form": perm_address_form,
            "text_input_attrs": text_input_attrs,
        }
        return render(request, self.template_name, context)


class SamajMemberEducationView(LoginRequiredMixin, View):
    template_name = "survey/education_form.html"

    def get(self, request: HttpRequest, member_id: int, *args, **kwargs):
        member = get_object_or_404(SamajMember, id=member_id)
        education_formset = SamajMemberEducationalQualificationFormSet(instance=member)
        context = {
            "member": member,
            "education_formset": education_formset,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, member_id: int, *args, **kwargs):
        member = get_object_or_404(SamajMember, id=member_id)
        education_formset = SamajMemberEducationalQualificationFormSet(
            request.POST, instance=member
        )

        if education_formset.is_valid():
            try:
                with transaction.atomic():
                    education_formset.instance = member
                    education_formset.save()
                    messages.success(
                        request, "Educational Qualification Saved Successfully!"
                    )
                    return redirect(
                        reverse(
                            "survey:occupation_form", kwargs={"member_id": member.id}
                        )
                    )
            except Exception as e:
                messages.error(request, f"There was an unexpected error: {e}")
        else:
            messages.error(request, "Please correct the errors below.")

        context = {
            "member": member,
            "education_formset": education_formset,
        }
        return render(request, self.template_name, context)


class SamajMemberOccupationView(LoginRequiredMixin, View):
    template_name = "survey/occupation_form.html"

    def get(self, request: HttpRequest, member_id: int, *args, **kwargs):
        member = get_object_or_404(SamajMember, id=member_id)
        occupation_instance = member.occupations.first()
        form = SamajMemberOccupationForm(instance=occupation_instance)
        context = {
            "member": member,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, member_id: int, *args, **kwargs):
        member = get_object_or_404(SamajMember, id=member_id)
        occupation_instance = member.occupations.first()
        form = SamajMemberOccupationForm(request.POST, instance=occupation_instance)

        if form.is_valid():
            try:
                with transaction.atomic():
                    occupation = form.save(commit=False)
                    occupation.member = member
                    occupation.save()
                    messages.success(request, "Occupation Details Saved Successfully!")
                    return redirect(
                        reverse("survey:income_form", kwargs={"member_id": member.id})
                    )
            except Exception as e:
                messages.error(request, f"There was an unexpected error: {e}")
        else:
            messages.error(request, "Please correct the errors below.")

        context = {
            "member": member,
            "form": form,
        }
        return render(request, self.template_name, context)


class SamajMemberIncomeView(LoginRequiredMixin, View):
    template_name = "survey/income_form.html"

    def get(self, request: HttpRequest, member_id: int, *args, **kwargs):
        member = get_object_or_404(SamajMember, id=member_id)
        income_instance = member.income.first()
        form = SamajMemberIncomeForm(instance=income_instance)
        context = {
            "member": member,
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest, member_id: int, *args, **kwargs):
        member = get_object_or_404(SamajMember, id=member_id)
        income_instance = member.income.first()
        form = SamajMemberIncomeForm(request.POST, instance=income_instance)

        if form.is_valid():
            try:
                with transaction.atomic():
                    income = form.save(commit=False)
                    income.member = member
                    income.save()
                    messages.success(request, "Income Details Saved Successfully!")
                    return redirect(reverse("survey:survey_sucess"))
            except Exception as e:
                messages.error(request, f"There was an unexpected error: {e}")
        else:
            messages.error(request, "Please correct the errors below.")

        context = {
            "member": member,
            "form": form,
        }
        return render(request, self.template_name, context)


def accept_terms(request: HttpRequest):
    if request.method == "POST":
        form = AcceptTermsForm(request.POST)
        if form.is_valid():
            request.session["terms_accepted"] = True
            messages.success(
                request, "Terms and Conditions accepted. You can now proceed."
            )
            return redirect(reverse("survey:personal_info_form"))
        else:
            messages.error(
                request, "Please accept all terms and conditions to proceed."
            )
    else:
        form = AcceptTermsForm()

    context = {"form": form}
    return render(request, "terms-conditions.html", context)


class SamajMemberOnboardingView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        if request.session.get("terms_accepted"):
            return redirect(reverse("survey:personal_info_form"))
        else:
            return redirect(reverse("survey:accept_terms"))


@login_required
def hx_perm_district_select(request: HttpRequest):
    context = {}
    state_id = request.GET.get("perm_state")
    if state_id:
        context["districts"] = District.objects.filter(state_id=state_id).order_by(
            "name"
        )
    return render(request, "survey/hx/perm_district_select.html", context)


@login_required
def hx_corr_district_select(request: HttpRequest):
    context = {}
    state_id = request.GET.get("corr_state")
    if state_id:
        context["districts"] = District.objects.filter(state_id=state_id).order_by(
            "name"
        )
    return render(request, "survey/hx/corr_district_select.html", context)


@login_required
def hx_corr_taluka_select(request: HttpRequest):
    context = {}
    district_id = request.GET.get("corr_district")
    if district_id:
        context["talukas"] = Taluka.objects.filter(district_id=district_id).order_by(
            "name"
        )
    return render(request, "survey/hx/corr_taluka_select.html", context)


@login_required
def hx_perm_taluka_select(request: HttpRequest):
    context = {}
    district_id = request.GET.get("perm_district")
    if district_id:
        context["talukas"] = Taluka.objects.filter(district_id=district_id).order_by(
            "name"
        )
    return render(request, "survey/hx/perm_taluka_select.html", context)


@login_required
def hx_corr_city_select(request: HttpRequest):
    context = {}
    district_id = request.GET.get("corr_district")
    if district_id:
        context["cities"] = City.objects.filter(district_id=district_id).order_by(
            "name"
        )
    return render(request, "survey/hx/corr_city_select.html", context)


@login_required
def hx_perm_city_select(request: HttpRequest):
    context = {}
    district_id = request.GET.get("perm_district")
    if district_id:
        context["cities"] = City.objects.filter(district_id=district_id).order_by(
            "name"
        )
    return render(request, "survey/hx/perm_city_select.html", context)


@login_required
def check_mobile_exists(request: HttpRequest) -> JsonResponse:
    mobile_no = request.GET.get("mobile_number")
    is_exist = SamajMemberMobileNumber.objects.filter(mobile_number=mobile_no).exists()
    return JsonResponse({"exists": is_exist})