# Generated by Django 5.1.1 on 2024-09-28 17:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Courses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Введите название курса', max_length=255, null=True, verbose_name='Название курса')),
                ('preview', models.ImageField(blank=True, help_text='Загрузите картинку курса', null=True, upload_to='courses/preview/', verbose_name='Превью курса')),
                ('description', models.TextField(blank=True, help_text='Введите описание курса', null=True, verbose_name='Описание курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Введите название урока', max_length=255, null=True, verbose_name='Название урока')),
                ('description', models.TextField(blank=True, help_text='Введите описание урока', null=True, verbose_name='Описание урока')),
                ('preview', models.ImageField(blank=True, help_text='Загрузите картинку урока', null=True, upload_to='courses/lesson/preview/', verbose_name='Превью урока')),
                ('video_link', models.URLField(blank=True, help_text='Введите ссылку на видео урока', null=True, verbose_name='Ссылка на видео урока')),
                ('course', models.ForeignKey(blank=True, help_text='Выберите Курс к уроку', null=True, on_delete=django.db.models.deletion.SET_NULL, to='materials.courses', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
            },
        ),
    ]