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
