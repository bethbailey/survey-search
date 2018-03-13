# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Test(models.Model):

    index_num = models.IntegerField(db_column='Index_Num', primary_key = True)  # Field name made lowercase.
    survey_id = models.CharField(db_column='Survey_ID', max_length = 200)  # Field name made lowercase.
    var_name = models.CharField(db_column='Var_Name', max_length = 200)  # Field name made lowercase.
    var_text = models.CharField(db_column='Var_Text', max_length = 500)  # Field name made lowercase.

    def __str__(self):
    	return self.var_text

    class Meta:
        managed = False
        db_table = 'test'
