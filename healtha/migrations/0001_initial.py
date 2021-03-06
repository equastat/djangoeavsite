# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-05 04:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_completed', models.DateTimeField(null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='healtha.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=250)),
                ('question_type', models.CharField(choices=[('StringValue', 'String'), ('IntegerValue', 'Integer')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.TextField()),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healtha.Participant')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='healtha.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('survey_name', models.CharField(max_length=250)),
                ('questions', models.ManyToManyField(to='healtha.Question')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='survey',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='healtha.Survey'),
        ),
        migrations.AlterUniqueTogether(
            name='questionresponse',
            unique_together=set([('participant', 'question')]),
        ),
    ]
