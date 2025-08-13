
from django.urls import path

from .views import (check_mobile_exists, hx_corr_taluka_select, hx_perm_district_select,
                    hx_corr_district_select, hx_perm_taluka_select, profile_completion, samaj_survey, survey_sucess,)

app_name = "survey"

urlpatterns = [
    path('', samaj_survey, name='survey_form'),
    path('profile-completion/', profile_completion, name='profile_completion'),
    path('check-mobile-exists/', check_mobile_exists, name="check-mobile-exists"),
    path('hx/perm-district/', hx_perm_district_select, name="hx_district_select"),
    path('hx/corr-district/', hx_corr_district_select,
         name="hx_corr_district_select"),
    path('hx/perm-taluka/', hx_perm_taluka_select, name="hx_taluka_select"),
    path('hx/corr-taluka/', hx_corr_taluka_select,
         name="hx_corr_taluka_select"),
    path('success/', survey_sucess, name="survey_sucess"),
]
