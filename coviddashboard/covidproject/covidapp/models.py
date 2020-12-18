# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Regions(models.Model):
    regionid = models.IntegerField(db_column='regionID', primary_key=True)  # Field name made lowercase.
    regionname = models.CharField(db_column='regionName', max_length=8, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'regions'
        verbose_name_plural = 'Regions'

class Provinces(models.Model):
    provinceid = models.AutoField(db_column='provinceID', primary_key=True)  # Field name made lowercase.
    regionid = models.ForeignKey('Regions', models.DO_NOTHING, db_column='regionID', blank=True, null=True)  # Field name made lowercase.
    provincename = models.CharField(db_column='provinceName', max_length=14, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'provinces'
        verbose_name_plural = 'Provinces'

class Cases(models.Model):
    caseid = models.AutoField(db_column='caseID', primary_key=True)  # Field name made lowercase.
    casedate = models.DateField(db_column='caseDate', blank=True, null=True)  # Field name made lowercase.
    caseprovinceid = models.ForeignKey('Provinces', models.DO_NOTHING, db_column='caseProvinceID', blank=True, null=True)  # Field name made lowercase.
    caseregionid = models.ForeignKey('Regions', models.DO_NOTHING, db_column='caseRegionID', blank=True, null=True)  # Field name made lowercase.
    caseagegroup = models.CharField(db_column='caseAgeGroup', max_length=5, blank=True, null=True)  # Field name made lowercase.
    casesex = models.CharField(db_column='caseSex', max_length=1, blank=True, null=True)  # Field name made lowercase.
    cases = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cases'
        verbose_name_plural = 'Cases'

class Hosps(models.Model):
    hospid = models.AutoField(db_column='hospID', primary_key=True)  # Field name made lowercase.
    hospdate = models.DateField(db_column='hospDate')  # Field name made lowercase.
    hospprovinceid = models.ForeignKey('Provinces', models.DO_NOTHING, db_column='hospProvinceID', blank=True, null=True)  # Field name made lowercase.
    hospregionid = models.ForeignKey('Regions', models.DO_NOTHING, db_column='hospRegionID', blank=True, null=True)  # Field name made lowercase.
    totalinhosp = models.IntegerField(db_column='totalInHosp', blank=True, null=True)  # Field name made lowercase.
    totalinicu = models.IntegerField(db_column='totalInICU', blank=True, null=True)  # Field name made lowercase.
    totalinresp = models.IntegerField(db_column='totalInResp', blank=True, null=True)  # Field name made lowercase.
    newinhosp = models.IntegerField(db_column='newInHosp', blank=True, null=True)  # Field name made lowercase.
    newouthosp = models.IntegerField(db_column='newOutHosp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hosps'
        verbose_name_plural = 'Hospitalisations'
        
class Deaths(models.Model):
    deathid = models.AutoField(db_column='deathID', primary_key=True)  # Field name made lowercase.
    deathdate = models.DateField(db_column='deathDate')  # Field name made lowercase.
    deathregionid = models.ForeignKey('Regions', models.DO_NOTHING, db_column='deathRegionID', blank=True, null=True)  # Field name made lowercase.
    deathagegroup = models.CharField(db_column='deathAgeGroup', max_length=5, blank=True, null=True)  # Field name made lowercase.
    deathsex = models.CharField(db_column='deathSex', max_length=1, blank=True, null=True)  # Field name made lowercase.
    deaths = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deaths'
        verbose_name_plural = 'Deaths'

class Tests(models.Model):
    testid = models.AutoField(db_column='testID', primary_key=True)  # Field name made lowercase.
    testdate = models.DateField(db_column='testDate', blank=True, null=True)  # Field name made lowercase.
    testprovinceid = models.ForeignKey(Provinces, models.DO_NOTHING, db_column='testProvinceID', blank=True, null=True)  # Field name made lowercase.
    testregionid = models.ForeignKey(Regions, models.DO_NOTHING, db_column='testRegionID', blank=True, null=True)  # Field name made lowercase.
    testall = models.IntegerField(db_column='testAll', blank=True, null=True)  # Field name made lowercase.
    testpos = models.IntegerField(db_column='testPos', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tests'
        verbose_name_plural = 'Tests'
