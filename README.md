## Django REST Framework Complete Authentication API 

## To Run this Project follow below:

## Setup Instructions
To run this project, follow these steps:
<br>
### 1. Create a Virtual Environment
Creating a virtual environment helps to manage dependencies for your project. Run the following command to create a virtual environment named authenv:

    mkvirtualenv authenv


### 2. Activate the Virtual Environment
<br>
activate the newly created virtual environment <br>
    
    source authenv/bin/activate


### 3. Install Required Packages <br/>
Once the virtual environment is activated, install the necessary packages listed in requirements.txt: <br>

    pip install -r requirements.txt

### 4. Apply Migrations
Before running the server, apply the migrations to set up your database schema: <br>

    python manage.py makemigrations
    python manage.py migrate


### 5. Run the Development Server
Start the Django development server to serve your application: <br>

    python manage.py runserver


### Requirements

Ensure you have the following packages installed, as listed in requirements.txt: <br/>

asgiref==3.5.0 <br/>
Django==4.0.3 <br/>
django-cors-headers==3.11.0 <br/>
django-dotenv==1.4.2 <br/>
djangorestframework==3.13.1 <br/>
djangorestframework-simplejwt==5.1.0 <br/>
PyJWT==2.3.0 <br/>
pytz==2021.3 <br/>
sqlparse==0.4.2 <br/>
tzdata==2021.5 <br/>
