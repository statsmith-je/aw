# Generated by Django 4.2.11 on 2024-03-17 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CourseInfo', '0012_remove_course_dhs_competencies_remove_course_elos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='elo',
            name='key_words',
            field=models.CharField(default='', max_length=1000),
            preserve_default=False,
        ),
    ]
