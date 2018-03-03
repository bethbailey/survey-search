from django.shortcuts import render 	

import operator
from functools import reduce

from django.db.models import Q
from django.http import HttpResponse
from django.views import generic

from .models import SurveyDetails, SurveyQuestions

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
    