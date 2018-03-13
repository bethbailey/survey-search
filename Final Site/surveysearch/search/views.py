# python libraries
import operator
import random
import csv
import tempfile
import shutil
import datetime
import numpy as np
from functools import reduce

# django libraries
from django.shortcuts import render, render_to_response
from django.db.models import Q
from django.http import HttpResponse
from django.views import generic
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django import forms

# from other parts of our django app
from .forms import SurveyUploadForm
from .models import SurveyDetails, SurveyQuestions

# for ranking algorithm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# for generating wordcloud
#import matplotlib
import matplotlib.pyplot as plt
import wordcloud
from PIL import Image

#matplotlib.use('Agg')


class IndexView(generic.ListView):
    '''
    Class that defines the view for the index. Provides a generic view.
    Code Ownership: Modified
    '''
    template_name = 'search/index.html'
    context_object_name = 'head_values'

    def get_queryset(self):
        """
        Dummy method, not called in template.
        """
        return SurveyQuestions.objects.all()
 
class ResultsView(generic.ListView):
    '''
    Class that defines the view for the question search results.
    Code Ownership: Original
    '''
    template_name = 'search/search_results.html'
    context_object_name = 'Survey_Questions_List'
    # include pagination
    paginate_by = 10 

    def get_queryset(self):
        '''
        Given a user query string, processes the query and searches the 
        database for questions that include the strings specified, and 
        returns the objects, along with the corresponding survey names.
        '''
        result = SurveyQuestions.objects.all()

        query = self.request.GET.get('q')
        if query:
            # account for multiple keywords
            query_list = query.split()
            # case insensitive search of question text column
            result = result.filter(reduce(operator.and_, \
                (Q(var_text__icontains=q) for q in query_list)))
            if result:
                # if there are query results, invoke ranking
                return get_ranked_questions(result, query)
            else:
                return []
        else:
            return []

    def get_context_data(self, **kwargs):
        '''
        Adds the survey details as a context object in order to access the 
        survey name.
        '''
        context = super(ResultsView, self).get_context_data(**kwargs)
        context.update({
            'Survey_Details_List': SurveyDetails.objects.all(),
        })
        return context

class SurveyResultsView(generic.ListView):
    '''
    Class that defines the view for the survey search results. This class
    queries the question text in the SurveyQuestions model and the summary
    and survey_name in the SurveyDetails model to find surveys that contain
    the keywords.
    Code Ownership: Original
    '''
    template_name = 'search/search_results_survey.html'
    paginate_by = 10 

    def get_queryset(self):
        result = SurveyDetails.objects.all()
        result2 = SurveyQuestions.objects.all()

        query = self.request.GET.get('q1')
        if query:
            # Account for multiple keywords
            query_list = query.split()
            # Find results in the SurveyDetails model.
            result_summary = result.filter(reduce(operator.and_, \
                (Q(summary__icontains=q1) | Q(survey_name__icontains=q1)\
                 for q1 in query_list)))
            # Find results in the SurveyQuestions model.
            result_questions = result2.filter(reduce(operator.and_, \
                (Q(var_text__icontains=q1) for q1 in query_list)))
            # Convert results to lists in order to iterate over them.
            result_summary_ls = list(result_summary)
            result_questions_ls = list(result_questions)
            # Iterate over the questions returned to find the survey
            # details associated with that question.
            for item in result_questions_ls:
                q2 = item.survey_key
                # Filter out those keys.
                result_summary_2 = result.filter(survey_key = q2)
                result_summary_ls = result_summary_ls + list(result_summary_2)
            # Remove repeated surveys and convert back to a list.
            rv = list(set(result_summary_ls))
            # If there is no rv or no query, return an empty list.
            if rv:
                return get_ranked_surveys(rv, query)
            else:
                return []
        else:
            return []

class Browse(generic.ListView):
    '''
    Class that defines view to display all the survey results. This class
    gets all the surveys in the SurveyDetails model and returns all the 
    objects.
    Code Ownership: Original
    '''
    template_name = 'search/browse_surveys.html'
    paginate_by = 10 

    def get_queryset(self):
        result = SurveyDetails.objects.all()

        if result:
            return result
        else:
            return []

class DetailView(generic.DetailView):
    '''
    Class that defines the view for Survey details for each question.
    Code Ownership: Original
    '''
    template_name = 'search/detail.html'
    model = SurveyQuestions

    def get_context_data(self, **kwargs):
        '''
        Adds the survey details as a context object in order to access the 
        details objects.
        '''
        context = super(DetailView, self).get_context_data(**kwargs)
        context.update({
            'Survey_Details_List': SurveyDetails.objects.all(),
        })
        return context

class QuestionDetail(generic.DetailView):
    '''
    Class that defines the view for Survey details for each question from the
    question list.
    Code Ownership: Original
    '''
    template_name = 'search/question_list.html'
    model = SurveyDetails

    def get_context_data(self, **kwargs):
        '''
        Adds the survey questions as a context object in order to access the 
        questions objects.
        '''
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        context.update({
            'Survey_Questions_List': SurveyQuestions.objects.all(),
        })
        return context

class BrowseDetailView(generic.DetailView):
    '''
    Class that defines the view for Survey details for each survey from the
    browse surveys list.
    Code Ownership: Original
    '''
    template_name = 'search/browse_detail.html'
    model = SurveyDetails


def home(request):
    '''
    View for the homepage
    '''
    surveys = SurveyDetails.objects.all()
    return render(request, 'search/index.html')

def upload_success(request):
    '''
    Show a confirmation of successful user upload
    '''
    return render(request, 'search/upload_success.html')

def upload_failure(request):
    '''
    Show a confirmation of failed user upload with error messages
    '''
    return render(request, 'search/upload_failure.html')

def model_form_upload(request):
    '''
    The view for displaying the page for users to upload surveys
    Code ownership: Original
    '''
    if request.method == 'POST':
        form = SurveyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            details = SurveyDetails()
            current_objects = list(SurveyDetails.objects.all())
            unique_upload = True
            csv_upload = True
            # initialize error message dictionaries to return unique error 
            # messages
            error_dict = {"csv": "", "unique": ""}
            # check for valid csv upload and duplicate survey names
            if request.FILES['survey_questions_document'].name[-3:] != "csv":
                csv_upload = False
                error_dict["csv"] = "Please upload a .csv file."
            for item in current_objects:
                if item.survey_name == data['survey_name']:
                    unique_upload = False
                    error_dict["unique"] = \
                        "This survey already exists in the database."
            if unique_upload and csv_upload:
                # adding unique index for each survey dataset
                id_obj = repr(datetime.datetime.utcnow())[17:] + " " + \
                    str(data['survey_name'])[0:3]
                details.survey_key = id_obj
                details.survey_name = data['survey_name']
                details.num_participants = data['num_participants']
                details.org_conduct = data['org_conduct']
                details.num_questions = data['num_questions']
                details.data_link = data['data_link']
                details.doc_link = data['doc_link']
                details.source_link = data['source_link']
                details.summary = data['summary']
                details.survey_questions_document = \
                    data['survey_questions_document']
                details.save()
                handle_files('documents/' + \
                    request.FILES['survey_questions_document'].name, id_obj)
                generate_wordcloud()

                return redirect('upload_success.html')
            else:
                # render error messages to failure page
                return render_to_response('search/upload_failure.html', \
                    error_dict)
    else:
        form = SurveyUploadForm()
    return render(request, 'search/upload.html', {
        'form': form
    })

def get_rankings(data, query):
    '''
    Given list of indices, texts correspond to those indices, and a query 
    string, return the indices ranked according to the tf-idf of the texts 
    and cosine similarities scores between the query string and the texts
    Inputs:
        data: a list of list in the format of [[indices],[texts]]
        query: a string containing the query keywords separated by space, 
            for example: "science religion research"
    Returns:
        ranked indices of the texts

    Code ownership: Original

    Reference for the algorithm:
    http://www.ardendertat.com/2011/07/17/how-to-implement-a-search-engine
        -part-3-ranking-tf-idf/
    '''

    data[1].append(query)
    tfidf_vectorizer = TfidfVectorizer(norm = "l1")
    tfidf_matrix = tfidf_vectorizer.fit_transform(data[1])  # finds the tfidf 
        # score with normalization
    cosine_scores = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix)
    del data[1][-1]
    data.append(list(cosine_scores[0]))
    arr = np.array(list(map(list, zip(*data))))
    arr = arr[arr[:, 2].argsort()]
    arr = arr[::-1]
    return arr[:, 0]

def get_ranked_questions(queries_results, query):
    '''
    Rank questions by their relevancy to the query string
    Code Ownership: Original
    '''
    data = [[s[0] for s in queries_results.values_list('row_num')]]
    data.append([s[0] for s in queries_results.values_list('var_text')])
    rankings = get_rankings(data, query)
    results = []
    for i in rankings:
        results.append(SurveyQuestions.objects.get(pk=i))
    return results

def get_ranked_surveys(queries_results, query):
    '''
    Rank surveys by their relevancy to the query string
    Code Ownership: Original
    '''
    data = [[s.survey_num for s in queries_results]]
    data.append([s.survey_name for s in queries_results])
    data.append([s.summary for s in queries_results])
    for i in range(len(data[0])):
        data[1][i] = data[1][i] + " " + data[2][i]
    del data[2]
    rankings = get_rankings(data, query)
    results = []
    for i in rankings:
        results.append(SurveyDetails.objects.get(pk=i))
    return results

def handle_files(csv_file, id_obj):
    '''
    Handles the file containing survey questions that user uploads:
    read the file and add questions to database
    Code Ownership: Modified
    '''
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            if str(row[0]).lower() != "var_name" and str(row[1]).lower() \
                != "var_text":
                questions = SurveyQuestions()
                questions.survey_key = id_obj
                questions.var_name = row[0]
                questions.var_text = row[1]
                questions.save()
        f.close()

def grey_color_func(word, font_size, position, orientation, random_state=None,
                    **kwargs):
    '''
    Generate random grey colors for plotting wordcloud
    Code Ownership: Direct Copy
    '''
    return "hsl(0, 0%%, %d%%)" % random.randint(0, 30)


def generate_wordcloud():
    '''
    Generate a word cloud from the words in the name and summary of all the 
    surveys in the database, called every time a survey is uploaded to the 
    database.

    Code Ownership: Original structure with reference to documentation and 
    online sources for implementing individual tasks
    '''

    # find words to include in wordcloud
    surveys = " ".join(s[0] for s in list(SurveyDetails.objects.values_list\
        ('summary')))
    surveys_names = " ".join(s[0] for s in \
        list(SurveyDetails.objects.values_list('survey_name')))
    text = surveys + " " + surveys_names

    # generate wordcloud and save to an image file
    wc = wordcloud.WordCloud(background_color="black",
                             max_words=500, width=2000, height=1500,
                             mode='RGBA', scale=1)
    wc.generate(text)
    plt.axis("off")

    # reference: https://stackoverflow.com/questions/14908576/how-to-remove
    # -frame-from-matplotlib-pyplot-figure-vs-matplotlib-figure-frame
    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.figure(figsize =(40, 30))
    a=plt.gca()
    a.set_frame_on(False)
    a.set_xticks([]); a.set_yticks([])

    # reference: https://github.com/amueller/word_cloud/tree/master/examples
    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),
           interpolation="bilinear")
    plt.savefig("search/static/img/wordcloud.png", format='png', \
        transparent = True, bbox_inches = 'tight', pad_inches = 0)
    plt.close()
