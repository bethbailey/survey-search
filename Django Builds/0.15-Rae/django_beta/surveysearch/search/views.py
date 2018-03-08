from django.shortcuts import render 	

import operator
from functools import reduce
from itertools import chain
import random

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

import numpy as np

from search.models import SurveyDetails
from search.forms import SurveyUploadForm
import matplotlib.pyplot as plt
import matplotlib
from PIL import Image
import wordcloud


matplotlib.use('Agg')


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
        	return []

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context.update({
            'Survey_Details_List': SurveyDetails.objects.all(),
        })
        return context

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
            return []

class Browse(generic.ListView):
    template_name = 'search/browse_surveys.html'
    paginate_by = 10 

    def get_queryset(self):
        result = SurveyDetails.objects.all()

        if result:
            return result
        else:
            return []

class DetailView(generic.DetailView):
    template_name = 'search/detail.html'
    model = SurveyQuestions

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update({
            'Survey_Details_List': SurveyDetails.objects.all(),
        })
        return context


class BrowseDetailView(generic.DetailView):
    template_name = 'search/browse_detail.html'
    model = SurveyDetails
from django import forms


def home(request):
    surveys = SurveyDetails.objects.all()
    return render(request, 'search/index.html')

def upload_success(request):
    return render(request, 'search/upload_success.html')

def model_form_upload(request):
    if request.method == 'POST':
        form = SurveyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            details = SurveyDetails()
            # adding unique index for each survey dataset
            id_obj = repr(datetime.datetime.utcnow())[17:] + " " + str(data['survey_name'])[0:3]
            details.survey_key = id_obj
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
            handle_files('documents/' + request.FILES['survey_questions_document'].name, id_obj)
            generate_wordcloud()
            print()
            return redirect('upload_success.html')
    else:
        form = SurveyUploadForm()
    return render(request, 'search/upload.html', {
        'form': form
    })


#http://www.ardendertat.com/2011/07/17/how-to-implement-a-search-engine-part-3-ranking-tf-idf/
#https://stackoverflow.com/questions/6473679/transpose-list-of-lists
def get_rankings(data, query):

    data[1].append(" ".join(keywords))
    tfidf_vectorizer = TfidfVectorizer()

    tfidf_matrix = tfidf_vectorizer.fit_transform(data[1])  # finds the tfidf score with normalization
    cosine_scores = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix)
    del data[1][-1]
    data.append(list(cosine_scores[0]))
    arr = np.array(list(map(list, zip(*data))))
    arr = arr[arr[:, 2].argsort()]
    arr = arr[::-1]
    return arr[:, 0]



def get_ranked_questions_index(queries_results, keywords):
    data = [[s[0] for s in queries_results.values_list('row_num')]]
    data.append([s[0] for s in queries_results.values_list('var_text')])
    return



def handle_files(csv_file, id_obj):
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            questions = SurveyQuestions()
            questions.survey_key = id_obj
            questions.var_name = row[0]
            questions.var_text = row[1]
            questions.save()
        f.close()


def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(0, 50)


def generate_wordcloud():

    questions = " ".join(s[0] for s in list(SurveyQuestions.objects.values_list('var_text')))
    surveys = " ".join(s[0] for s in list(SurveyDetails.objects.values_list('summary')))
    surveys_names = " ".join(s[0] for s in list(SurveyDetails.objects.values_list('survey_name')))
    text = surveys + " " + surveys_names
    mask = np.array(Image.open("search/static/img/mask.png"))

    wc = wordcloud.WordCloud(background_color="black", max_words=500, width=2000, height=2000, mode='RGBA',
                             scale=1)
    wc.generate(text)
    default_colors = wc.to_array()

    plt.figure(figsize=(40, 30))
    plt.axis("off")
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    a=plt.gca()
    a.set_frame_on(False)
    a.set_xticks([]); a.set_yticks([])

    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")

    plt.savefig("search/static/img/wordcloud.png", format='png', transparent = True,
                bbox_inches = 'tight', pad_inches = 0)

    plt.close()
