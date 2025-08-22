from django.urls import path

from .views import (check_mobile_exists, hx_corr_taluka_select, hx_perm_district_select,
                    hx_corr_district_select, hx_perm_taluka_select, profile_completion, survey_sucess,
                    SamajMemberCreateView, SamajMemberAddressView, SamajMemberEducationView,
                    SamajMemberOccupationView, SamajMemberIncomeView,
                    accept_terms, SamajMemberOnboardingView, hx_corr_city_select, hx_perm_city_select)

app_name = "survey"

urlpatterns = [
    path('', SamajMemberOnboardingView.as_view(), name='samaj_member_onboarding'),
    path('personal-info/', SamajMemberCreateView.as_view(), name='personal_info_form'),
    path('member/<int:member_id>/address/', SamajMemberAddressView.as_view(), name='address_form'),
    path('member/<int:member_id>/education/', SamajMemberEducationView.as_view(), name='education_form'),
    path('member/<int:member_id>/occupation/', SamajMemberOccupationView.as_view(), name='occupation_form'),
    path('member/<int:member_id>/income/', SamajMemberIncomeView.as_view(), name='income_form'),

    path('accept-terms/', accept_terms, name='accept_terms'),

    path('profile-completion/', profile_completion, name='profile_completion'),
    path('check-mobile-exists/', check_mobile_exists, name="check-mobile-exists"),
    path('hx/perm-district/', hx_perm_district_select, name="hx_district_select"),
    path('hx/corr-district/', hx_corr_district_select,
         name="hx_corr_district_select"),
    path('hx/perm-taluka/', hx_perm_taluka_select, name="hx_taluka_select"),
    path('hx/perm-district/', hx_perm_district_select, name="hx_perm_district_select"),
    path('hx/corr-district/', hx_corr_district_select, name="hx_corr_district_select"),
    path('hx/perm-taluka/', hx_perm_taluka_select, name="hx_perm_taluka_select"),
    path('hx/corr-taluka/', hx_corr_taluka_select, name="hx_corr_taluka_select"),
    path('hx/perm-city/', hx_perm_city_select, name="hx_perm_city_select"),
    path('hx/corr-city/', hx_corr_city_select, name="hx_corr_city_select"),
    path('hx/perm-state/', hx_perm_state_select, name="hx_perm_state_select"),
    path('hx/corr-state/', hx_corr_state_select, name="hx_corr_state_select"),
    path('hx/perm-city/', hx_perm_city_select, name="hx_perm_city_select"),
    path('hx/corr-city/', hx_corr_city_select,
         name="hx_corr_city_select"),
    path('success/', survey_sucess, name="survey_sucess"),
]