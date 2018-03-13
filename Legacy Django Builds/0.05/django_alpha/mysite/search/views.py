from django.shortcuts import render

import operator
from functools import reduce

from django.db.models import Q
from django.http import HttpResponse
from django.views import generic

from .models import Test

class IndexView(generic.ListView):
    template_name = 'search/index.html'
    context_object_name = 'head_values'

    def get_queryset(self):
        """
        Dummy method, not called in template.
        """
        return Test.objects.all()
 
class ResultsView(generic.ListView):
    template_name = 'search/search_results.html'
    paginate_by = 10 

    def get_queryset(self):
        result = Test.objects.all()

        query = self.request.GET.get('q')
        if query:
            query_list = query.split()
            result = result.filter(reduce(operator.and_, (Q(var_text__icontains=q) for q in query_list)))
            
            return result
        else:
        	pass

class DetailView(generic.DetailView):
    template_name = 'search/detail.html'
    model = Test
   