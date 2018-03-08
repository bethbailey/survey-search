from django import forms

from search.models import SurveyDetails


class SurveyUploadForm(forms.ModelForm):

    summary = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = SurveyDetails
        fields = ('survey_name', 'num_participants',\
        'org_conduct', 'num_questions', 'data_link', 'doc_link', 'source_link', \
        'summary', 'survey_questions_document')

    def __init__(self, *args, **kwargs):
        super(SurveyUploadForm, self).__init__(*args, **kwargs)
        self.fields['summary'].widget.attrs['cols'] = 40
        self.fields['summary'].widget.attrs['rows'] = 10