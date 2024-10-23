from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from config.settings import EMAIL_HOST_USER

from materials.models import Courses
from users.models import Subscription, User


@shared_task
def send_message_course_update(course_id):
    """ отправляет сообщения об изменении, внесенном в курс, на которые подписан user """

    # делаем через проверку
    try:
        print(f'Processing course_id: {course_id}')
        course = Courses.objects.get(pk=course_id)  # Извлекаем курс
        print(f'Course: {course}')

        # Получаем подписки на курс
        subscriptions = Subscription.objects.filter(course=course)
        print(f'Subscriptions: {subscriptions}')

        # Формируем список email
        email_list = [subscription.user.email for subscription in subscriptions]

        if email_list:
            send_mail(
                subject=f'Обновлен материал курса: {course.name}',
                message=f"Уведомляем вас о том, что материалы курса {course.name} были обновлены.",
                from_email=EMAIL_HOST_USER,
                recipient_list=email_list
            )
            print(f'Emails sent to: {email_list}')
        else:
            print(f'No subscribers for course {course.name}')

    except Courses.DoesNotExist:
        print(f'Course with id {course_id} does not exist.')
    except Exception as e:
        print(f'Error in send_message_course_update: {e}')


@shared_task
def deactivate_inactive_users():
    """Деактивирует пользователей, которые не заходили более месяца."""

    # Определяем дату для сравнения — один месяц назад
    one_month_ago = timezone.now() - timedelta(days=30)  # timedelta(minutes=5) для теста

    # Выбираем пользователей, которые не заходили более месяца
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    # Деактивируем таких пользователей
    inactive_users.update(is_active=False)

    # принтим результат
    print(f"Deactivated {inactive_users.count()} inactive users.")
    print(f"Inactive users: {inactive_users}")

