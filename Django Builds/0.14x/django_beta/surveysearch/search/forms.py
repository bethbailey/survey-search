from django import forms

from search.models import SurveyDetails


class SurveyUploadForm(forms.ModelForm):
    class Meta:
        model = SurveyDetails
        fields = ('survey_name', 'num_participants',\
        'org_conduct', 'num_questions', 'data_link', 'doc_link', 'source_link', \
        'summary', 'survey_questions_document')