start:
	python3 manage.py runserver

run_celery:
	celery -A website  worker -l info