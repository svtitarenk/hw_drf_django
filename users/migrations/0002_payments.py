# Generated by Django 5.1.1 on 2024-09-29 17:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_date', models.DateField(auto_now_add=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('payment_type', models.CharField(choices=[('cash', 'наличные'), ('transfer', 'перевод на счет')], help_text='Выберите тип оплаты', max_length=10, verbose_name='тип оплаты')),
                ('course', models.ForeignKey(blank=True, help_text='Выберите курс', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course', to='materials.courses', verbose_name='Курс')),
                ('lesson', models.ForeignKey(blank=True, help_text='Выберите урок', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='materials.lesson', verbose_name='Урок')),
                ('user', models.ForeignKey(help_text='Введите имя пользователя', on_delete=django.db.models.deletion.CASCADE, related_name='user_payment', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
