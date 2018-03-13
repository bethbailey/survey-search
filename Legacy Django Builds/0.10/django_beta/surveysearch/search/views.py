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


def model_form_upload(request):
    if request.method == 'POST':
        form = SurveyUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('search/index.html')
    else:
        form = SurveyUploadForm()
    return render(request, 'search/upload.html', {
        'form': form
    })