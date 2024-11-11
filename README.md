# hw_drf_django
Homework drf djano


### работают следующие команды для Windows с celery и celery-beat
`celery -A config worker --loglevel=info -E -P eventlet`

`celery -A config beat -l info -S django`

Запуск docker-compose:
  `docker-compose up -d --build`
