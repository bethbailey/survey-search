from django.shortcuts import render 	

import operator
from functools import reduce

from django.db.models import Q
from django.http import HttpResponse
from django.views import generic

from .models import SurveyDetails, SurveyQuestions
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from search.models import SurveyDetails
from search.forms import SurveyUploadForm
import csv
import tempfile
import shutil

class IndexView(generic.ListView):
    template_name = 'search/index.html'
    context_object_name = 'head_values'

    def get_queryset(self):
        """
        Dummy method, not called in template.
        """
        return SurveyQuestions.objects.all()
 
class ResultsView(generic.ListView):
    template_name = 'search/search_results.html'
    context_object_name = 'Survey_Questions_List'
    paginate_by = 10 

    def get_queryset(self):
        result = SurveyQuestions.objects.all()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_, (Q(var_text__icontains=q) for q in query_list)))
            
            return result
        else:
        	pass

class SurveyResultsView(generic.ListView):
    template_name = 'search/search_results_survey.html'
    paginate_by = 10 

    def get_queryset(self):
        result = SurveyDetails.objects.all()

        query = self.request.GET.get('q1')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_, (Q(summary__icontains=q1) for q1 in query_list)))
            
            return result
        else:
            pass

class DetailView(generic.DetailView):
    template_name = 'search/detail.html'
    # context_object_name = 'Survey_Details_List'
    model = SurveyQuestions

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update({
            'Survey_Details_List': SurveyDetails.objects.all(),
        })
        return context


from django import forms


def home(request):
    surveys = SurveyDetails.objects.all()
    return render(request, 'search/index.html')

def upload_success(request):
    return render(request, 'search/upload_success.html')

def browse_surveys(request):
    return render(request, 'search/browse_surveys.html')

def model_form_upload(request):
    if request.method == 'POST':
        form = SurveyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            handle_files('documents/' + request.FILES['survey_questions_document'].name)
            print()
            return redirect('upload_success.html')
    else:
        form = SurveyUploadForm()
    return render(request, 'search/upload.html', {
        'form': form
    })


def handle_files(csv_file):
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            questions = SurveyQuestions()
            questions.row_num = row[0]
            questions.survey_num = row[1]
            questions.survey_id = row[2]
            questions.survey_name = row[3]
            questions.var_name = row[4]
            questions.var_text = row[5]
            questions.data_link = row[6]
            questions.save()
        f.close()

def generate_wordcloud():
    surveys = SurveyDetails.objects.all()

    pass

