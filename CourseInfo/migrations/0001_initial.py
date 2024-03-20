# Generated by Django 5.0.3 on 2024-03-20 01:17

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Competency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competency', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=1000)),
                ('cadre', models.CharField(max_length=1000)),
                ('cadre_acronym', models.CharField(default='', max_length=10)),
                ('position', models.CharField(default='', max_length=1000)),
                ('position_acronym', models.CharField(max_length=1000)),
                ('ptb_course', models.BooleanField(default=True)),
                ('dhs_comp', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testfile', models.FileField(upload_to='', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['docx'])], verbose_name='Testbank spreadsheet')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=1000)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TLO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tlo', models.CharField(max_length=1000)),
                ('key_words', models.CharField(blank=True, max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ELO',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elo', models.CharField(max_length=1000)),
                ('key_words', models.CharField(max_length=1000)),
                ('dhs_competency', models.ManyToManyField(blank=True, to='CourseInfo.competency')),
            ],
        ),
        migrations.CreateModel(
            name='PTB',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ptb', models.IntegerField()),
                ('description', models.CharField(max_length=1000)),
                ('elos', models.ManyToManyField(blank=True, to='CourseInfo.elo')),
            ],
        ),
        migrations.AddField(
            model_name='elo',
            name='ptbs',
            field=models.ManyToManyField(blank=True, to='CourseInfo.ptb'),
        ),
        migrations.CreateModel(
            name='TBItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=1000)),
                ('stem', models.CharField(max_length=1000)),
                ('options', models.JSONField()),
                ('justifications', models.JSONField()),
                ('correct_answer', models.CharField(max_length=1000)),
                ('competencies', models.ManyToManyField(blank=True, to='CourseInfo.competency')),
                ('course', models.ManyToManyField(blank=True, to='CourseInfo.course')),
                ('elos', models.ManyToManyField(to='CourseInfo.elo')),
                ('tlo', models.ManyToManyField(blank=True, to='CourseInfo.tlo')),
            ],
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_number', models.CharField(max_length=50)),
                ('module_title', models.CharField(max_length=1000)),
                ('minutes_to_complete', models.CharField(max_length=1000)),
                ('number_of_slides', models.IntegerField(blank=True)),
                ('number_of_activities', models.IntegerField(blank=True)),
                ('competencies', models.ManyToManyField(blank=True, to='CourseInfo.competency')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='CourseInfo.course')),
                ('elos', models.ManyToManyField(blank=True, to='CourseInfo.elo')),
                ('ptbs', models.ManyToManyField(blank=True, to='CourseInfo.ptb')),
                ('tb_items', models.ManyToManyField(blank=True, to='CourseInfo.tbitem')),
                ('tlos', models.ManyToManyField(blank=True, to='CourseInfo.tlo')),
            ],
        ),
    ]
