# wsgi-server
### for start server use this command:
*on windows*
* waitress-serve --listen localhost:8000 main:application

*on mac/linux*
* gunicorn --bind localhost:8000 main:application
