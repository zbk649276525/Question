# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-09 02:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', models.IntegerField(blank=True, null=True)),
                ('content', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='选项名称')),
                ('score', models.IntegerField(verbose_name='选项对应的分值')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=64)),
                ('tp', models.IntegerField(choices=[(1, '打分'), (2, '单选'), (3, '评价')])),
            ],
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('cls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ClassList')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
                ('cls', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.ClassList')),
            ],
        ),
        migrations.CreateModel(
            name='Userinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('pwd', models.CharField(max_length=32)),
            ],
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Userinfo'),
        ),
        migrations.AddField(
            model_name='option',
            name='qs',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app01.Option'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='stu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.Student'),
        ),
    ]
