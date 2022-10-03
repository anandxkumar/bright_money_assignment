start:
	python manage.py runserver

run_celery:
	celery -A mainApp  worker -l info