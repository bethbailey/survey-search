from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search_results.html', views.ResultsView.as_view(), name='results_detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='question_detail'),
]