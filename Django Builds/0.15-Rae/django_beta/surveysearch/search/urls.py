from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search_results.html', views.ResultsView.as_view(), \
    	name='results_detail'),
    path('search_results_survey.html', views.SurveyResultsView.as_view(), \
    	name='survey_results_detail'),
    path('<int:pk>/', views.DetailView.as_view(), name='question_detail'),
    path('upload.html', views.model_form_upload, name='upload'),
    path('upload_success.html', views.upload_success, name='upload_success'),
    path('browse_surveys.html', views.Browse.as_view(), name='browse_surveys')
]