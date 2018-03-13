from django.contrib import admin

from .models import SurveyDetails, SurveyQuestions
# Register your models here.
admin.site.register(SurveyDetails)
admin.site.register(SurveyQuestions)
