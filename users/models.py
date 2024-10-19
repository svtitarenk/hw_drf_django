from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Courses, Lesson

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта', help_text='Укажите почту')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='телефон', help_text='Укажите телефон')
    city = models.CharField(max_length=255, **NULLABLE, verbose_name='Город', help_text='укажите город')
    avatar = models.ImageField(upload_to='users/avatar/', **NULLABLE, verbose_name='Аватар',
                               help_text='Загрузите аватар')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer'

    PAYMENT_TYPE_CHOICES = [
        (CASH, 'наличные'),
        (TRANSFER, 'перевод на счет'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        help_text='Введите имя пользователя',
        related_name='user_payment',
        **NULLABLE
    )
    payment_date = models.DateField(auto_now_add=True)
    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        verbose_name='Курс',
        help_text='Выберите курс',
        related_name='courses',
        **NULLABLE
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name='Урок',
        help_text='Выберите урок',
        related_name='lessons',
        **NULLABLE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(
        max_length=10,
        choices=PAYMENT_TYPE_CHOICES,
        verbose_name='тип оплаты',
        help_text='Выберите тип оплаты'
    )

    def __stt__(self):
        return f'Платеж {self.payment_date} на курс {self.course} урок {self.lesson} на сумму: {self.amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Пользователь'
    )
    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Курс'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.course}'

    class Meta:
        unique_together = ('user', 'course')  # Уникальность подписки для пользователя и курса
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ['user']


class Payment(models.Model):
    amount = models.PositiveIntegerField(
        verbose_name='Сумма оплаты',
        help_text='Укажите сумму',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания',
        help_text='Дата создания оплаты',
        **NULLABLE,
    )
    session_id = models.CharField(
        max_length=255,
        **NULLABLE,
        verbose_name='id сессии',
        help_text='Укажите id сессии',
    )
    link = models.URLField(
        max_length=400,
        **NULLABLE,
        verbose_name='Ссылка на оплату',
        help_text='Укажите ссылку на оплату',
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        help_text='Укажите пользователя',
        on_delete=models.CASCADE,
        **NULLABLE,
    )
    course = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name='payment_course',
        verbose_name='Курс',
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
        ordering = ['user']

    def __str__(self):
        return f'{self.amount} руб. от {self.user}'

