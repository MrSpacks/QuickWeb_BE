run:
	cd quick_web && source .venv/bin/activate && cd .. && python manage.py runserver

test:
	cd quick_web && source .venv/bin/activate && cd .. && python manage.py test api