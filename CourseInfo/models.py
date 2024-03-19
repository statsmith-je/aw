from django.db import models
from django.db.models.signals import post_save
from django.core.validators import FileExtensionValidator

# from django.contrib.auth.models import Group
# Create your models here.

class File(models.Model):
    testfile = models.FileField(upload_to = "", verbose_name="Testbank spreadsheet", validators=[FileExtensionValidator(allowed_extensions=['docx'])])

#Users
class User(models.Model):
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    email = models.EmailField(max_length = 100)
    password = models.CharField(max_length = 50)

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'
    
#Competencies
class Competency(models.Model):
    competency = models.CharField(max_length = 50)
    description = models.CharField( max_length = 1000)

    def __str__(self):
        return self.competency
    

#PTBs
class PTB(models.Model):
    ptb = models.IntegerField()
    description = models.CharField( max_length = 1000)
    elos = models.ManyToManyField("ELO", blank = True)

    def __str__(self):
        return f'{self.ptb}'

#ELO
class ELO(models.Model):
    elo = models.CharField(max_length = 1000)
    ptbs = models.ManyToManyField(PTB, blank = True)
    dhs_competency = models.ManyToManyField("Competency", blank=True)
    key_words = models.CharField(max_length = 1000)

    def __str__(self):
        return self.elo


#TestBankItems
class TBItem(models.Model):
    code = models.CharField(max_length = 1000)
    stem = models.CharField( max_length = 1000)
    options = models.JSONField()
    justifications = models.JSONField()
    correct_answer = models.CharField( max_length = 1000)
    course = models.ManyToManyField("Course", blank = True)
    elos = models.ManyToManyField("ELO")
    competencies = models.ManyToManyField("Competency", blank = True)
    tlo = models.ManyToManyField("TLO", blank = True)
    

    def __str__(self):
        return self.stem


#TLO
class TLO(models.Model):
    tlo = models.CharField( max_length = 1000)
    key_words = models.CharField(max_length = 1000, blank = True)

    
    def __str__(self):
        return self.tlo


#Survey
class Survey(models.Model):
    code = models.CharField( max_length = 1000)
    date = models.DateField()
    
    def __str__(self):
        return self.code


#Course
class Course(models.Model):
    code = models.CharField( max_length = 1000)
    cadre = models.CharField(max_length = 1000)
    cadre_acronym = models.CharField(max_length = 10, default = "")
    position = models.CharField(max_length = 1000, default = "")
    position_acronym = models.CharField(max_length = 1000)
    
    ptb_course = models.BooleanField(default = True)
    dhs_comp = models.BooleanField(default = False)

    def __str__(self):
        return f'{self.cadre_acronym}: {self.position_acronym} ({self.code})'
    
#Modules
class Module(models.Model):
    course = models.ForeignKey(Course, on_delete = models.DO_NOTHING)
    module_number = models.CharField( max_length = 50)
    module_title = models.CharField( max_length = 1000)
    tlos = models.ManyToManyField(TLO, blank = True)
    elos = models.ManyToManyField(ELO, blank = True)
    ptbs = models.ManyToManyField(PTB, blank = True)
    competencies = models.ManyToManyField(Competency, blank = True)
    tb_items = models.ManyToManyField(TBItem , blank = True)
    minutes_to_complete = models.CharField(max_length = 1000)
    number_of_slides = models.IntegerField(blank = True)
    number_of_activities = models.IntegerField(blank = True)
    
    
    @property
    def course_name(self):
        return f'{self.course}-{self.module_number}'
    
    def __str__(self):
        return self.course_name


#users