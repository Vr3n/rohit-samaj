
from django.urls import path

from .views import (hx_corr_taluka_select, hx_perm_district_select,
                    hx_corr_district_select, hx_perm_taluka_select, samaj_survey, survey_sucess,)


urlpatterns = [
    path('', samaj_survey, name='survey_form'),
    path('hx/perm-district/', hx_perm_district_select, name="hx_district_select"),
    path('hx/corr-district/', hx_corr_district_select,
         name="hx_corr_district_select"),
    path('hx/perm-taluka/', hx_perm_taluka_select, name="hx_taluka_select"),
    path('hx/corr-taluka/', hx_corr_taluka_select,
         name="hx_corr_taluka_select"),
    path('success/', survey_sucess, name="survey_sucess"),
]
