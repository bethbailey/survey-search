# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SurveyDetails(models.Model):

    #row_num = models.IntegerField(db_column='row_num')
    survey_num = models.AutoField(db_column='survey_num', primary_key = True)
    #survey_id = models.CharField(db_column='survey_id', max_length = 200)
    survey_key = models.CharField(db_column = 'survey_key', max_length = 500)
    survey_name = models.CharField(db_column='survey_name', max_length = 1000)
    num_participants = models.IntegerField(db_column='num_participants')
    org_conduct = models.CharField(db_column='org_conduct', max_length = 1000)
    num_questions = models.IntegerField(db_column='num_questions')
    data_link = models.CharField(db_column='data_link', max_length = 1000)
    doc_link = models.CharField(db_column='doc_link', max_length = 1000)
    source_link = models.CharField(db_column='source_link', max_length = 1000)
    summary = models.CharField(db_column='summary', max_length = 3000)
    survey_questions_document = models.FileField(db_column="document", upload_to="documents/")
    #test = models.CharField(db_column='test', max_length=1000)

    def __str__(self):
        return self.summary

    class Meta:
        db_table = 'survey_details_new'


class SurveyQuestions(models.Model):

    row_num = models.AutoField(db_column='row_num', primary_key = True)
    #survey_name = models.CharField(db_column='survey_name', max_length = 1000)
    survey_key = models.CharField(db_column = 'survey_key', max_length = 500)
    var_name = models.CharField(db_column='var_name', max_length = 200)
    var_text = models.CharField(db_column='var_text', max_length = 1000)
    #data_link = models.CharField(db_column='data_link', max_length = 1000)

    def __str__(self):
        return self.var_text

    class Meta:
        db_table = 'survey_questions'

