from django.shortcuts import render 	

import operator
from functools import reduce
from itertools import chain

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
import datetime

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
        result2 = SurveyQuestions.objects.all()

        query = self.request.GET.get('q1')
        if query:
            query_list = query.split()
            result_summary = result.filter(reduce(operator.and_, (Q(summary__icontains=q1) for q1 in query_list)))
            result_questions = result2.filter(reduce(operator.and_, (Q(var_text__icontains=q1) for q1 in query_list)))
            result_summary_ls = list(result_summary)
            result_questions_ls = list(result_questions)
            for item in result_questions_ls:
                q2 = item.survey_key
                result_summary_2 = result.filter(survey_key = q2)
                result_summary_ls = result_summary_ls + list(result_summary_2)
            rv = list(set(result_summary_ls))
            return rv
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
            data = form.cleaned_data
            details = SurveyDetails()
            # adding unique index for each survey dataset
            id_obj = repr(datetime.datetime.utcnow())[17:] + " " + str(data['survey_name'])[0:3]
            #details.row_num = data['row_num']
            details.survey_key = id_obj
            #details.survey_id = data['survey_id']
            details.survey_name = data['survey_name']
            details.num_participants = data['num_participants']
            details.org_conduct = data['org_conduct']
            details.num_questions = data['num_questions']
            details.data_link = data['data_link']
            details.doc_link = data['doc_link']
            details.source_link = data['source_link']
            details.summary = data['summary']
            details.survey_questions_document = data['survey_questions_document']
            details.save()
            #form.save()
            handle_files('documents/' + request.FILES['survey_questions_document'].name, id_obj)
            print()
            return redirect('upload_success.html')
    else:
        form = SurveyUploadForm()
    return render(request, 'search/upload.html', {
        'form': form
    })


def handle_files(csv_file, id_obj):
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            questions = SurveyQuestions()
            #questions.row_num = row[0]
            questions.survey_key = id_obj
            #questions.survey_num = row[1]
            #questions.survey_id = row[2]
            #questions.survey_name = row[3]
            questions.var_name = row[4]
            questions.var_text = row[5]
            #questions.data_link = row[6]
            questions.save()
        f.close()


def generate_wordcloud():
    surveys = SurveyDetails.objects.all()

    pass

