from django.db import models

NULLABLE = {"blank": True, "null": True}


class Courses(models.Model):
    name = models.CharField(
        max_length=255, **NULLABLE,
        verbose_name='Название курса',
        help_text='Введите название курса'
    )
    preview = models.ImageField(
        upload_to='courses/preview/',
        **NULLABLE,
        verbose_name='Превью курса',
        help_text='Загрузите картинку курса'
    )
    description = models.TextField(
        **NULLABLE,
        verbose_name='Описание курса',
        help_text='Введите описание курса'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    course = models.ForeignKey(
        Courses,
        **NULLABLE,
        verbose_name='Курс',
        help_text='Выберите Курс к уроку',
        on_delete=models.SET_NULL,
        related_name='course'
    )
    name = models.CharField(
        max_length=255, **NULLABLE,
        verbose_name='Название урока',
        help_text='Введите название урока'
    )
    description = models.TextField(
        **NULLABLE,
        verbose_name='Описание урока',
        help_text='Введите описание урока'
    )
    preview = models.ImageField(
        upload_to='courses/lesson/preview/',
        **NULLABLE,
        verbose_name='Превью урока',
        help_text='Загрузите картинку урока'
    )
    video_link = models.URLField(
        **NULLABLE,
        verbose_name='Ссылка на видео урока',
        help_text='Введите ссылку на видео урока'
    )

    def __str__(self):
        return f'Урок: {self.name}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
