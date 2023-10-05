## Run celery and beat server
* celery -A hex_images worker --loglevel=info
* celery -A hex_images beat -l info

## coverage report

* coverage run manage.py test -v 2 && coverage report
