import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

# чтобы не вылезало постоянно предупреждение. Что это делает, непонятно )
app.conf.broker_connection_retry_on_startup = True


app.autodiscover_tasks()
