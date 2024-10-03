from django.core.management import BaseCommand
from users.models import Payments


class Command(BaseCommand):
    def handle(self, *args, **options):
        payments_list = [
            {'user_id': 1, 'payment_date': '2024-01-01', 'course_id': 1, 'lesson_id': 1, 'amount': 1000,
             'payment_type': 'cash'},
            {'user_id': 1, 'payment_date': '2024-02-01', 'course_id': 1, 'lesson_id': 1, 'amount': 1000,
             'payment_type': 'transfer'},
            {'user_id': 1, 'payment_date': '2024-03-01', 'course_id': 1, 'lesson_id': 1, 'amount': 1000,
             'payment_type': 'transfer'},
            {'user_id': 1, 'payment_date': '2024-01-01', 'course_id': 1, 'lesson_id': 2, 'amount': 2000,
             'payment_type': 'cash'},
            {'user_id': 1, 'payment_date': '2024-01-01', 'course_id': 1, 'lesson_id': 3, 'amount': 3000,
             'payment_type': 'cash'},
            {'user_id': 2, 'payment_date': '2023-01-01', 'course_id': 1, 'lesson_id': 1, 'amount': 1000,
             'payment_type': 'cash'},
            {'user_id': 2, 'payment_date': '2023-02-01', 'course_id': 1, 'lesson_id': 1, 'amount': 1000,
             'payment_type': 'transfer'},
            {'user_id': 2, 'payment_date': '2023-03-01', 'course_id': 1, 'lesson_id': 1, 'amount': 1000,
             'payment_type': 'transfer'},
            {'user_id': 2, 'payment_date': '2023-01-01', 'course_id': 1, 'lesson_id': 2, 'amount': 2000,
             'payment_type': 'cash'},
            {'user_id': 2, 'payment_date': '2023-01-01', 'course_id': 1, 'lesson_id': 3, 'amount': 3000,
             'payment_type': 'cash'},
        ]

        # payments_list = [
        #     {'user_id': 1, 'payment_date': '2024-01-01', 'course_id': 1, 'amount': 1000, 'payment_type': 'cash'}
        # ]

        # for student in student_list:
        #     Student.objects.create(**student)

        payments_for_create = []
        for payment_item in payments_list:
            # print('payment_date:', payment_item.get('payment_date'))
            payments_for_create.append(
                Payments(**payment_item)
            )

        Payments.objects.bulk_create(payments_for_create)
