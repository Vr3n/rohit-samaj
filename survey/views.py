from django.shortcuts import redirect, render
from django.http import HttpRequest

from survey.forms import SamajSurveyForm

# Create your views here.


def survey_sucess(request: HttpRequest):
    return render(request, 'survey_success.html')


def samaj_survey(request):
    if request.method == "POST":
        form = SamajSurveyForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('success_page')
        return render(request, 'survey/form.html', {'form': form})
    else:
        form = SamajSurveyForm()

    return render(request, 'survey/form.html', {'form': form})
