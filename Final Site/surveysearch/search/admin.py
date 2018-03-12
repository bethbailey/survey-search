# Code ownership: "Direct copy" 

from django.contrib import admin

from .models import SurveyDetails, SurveyQuestions

admin.site.register(SurveyDetails)
admin.site.register(SurveyQuestions)
