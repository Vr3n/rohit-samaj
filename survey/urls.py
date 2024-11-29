
from django.urls import path

from .views import samaj_survey, survey_sucess


urlpatterns = [
    path('', samaj_survey, name='survey_form'),
    path('success/', survey_sucess, name="survey_sucess"),
]
