## Django REST Framework Complete Authentication API

A sample server example to demonstrate the Django Rest Framework Authentication, sending and receiving data from the server. To run the project we first need to activate the virtual environment "authenv" and install the requirements. If the installation is done then we have to configure the database connection. Check the 'settings.py' to update the database connection configuration. After that migrate the database scheme using the following commands. Configure the SMTP email before running the project.


## To Run this Project follow below:

```bash
mkvirtualenv authenv
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

database connection required

## SMTP Email configuration
```
# Email Configuration
EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'email_host@gmail.com'
EMAIL_HOST_PASSWORD = 'email pass'
EMAIL_USE_TLS = True
```


## Requirements
```
asgiref==3.5.0
Django==4.0.3
django-cors-headers==3.11.0
django-dotenv==1.4.2
djangorestframework==3.13.1
djangorestframework-simplejwt==5.1.0
PyJWT==2.3.0
pytz==2021.3
sqlparse==0.4.2
tzdata==2021.5
```

#### There is a File "DjangoMyPathAPI.postman_collection" which has Postman Collection You can import this file in your postman to test this API

