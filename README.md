## Django REST Framework Complete Authentication API <br/>

## To Run this Project follow below: <br/>

## Setup Instructions
To run this project, follow these steps:

# 1. Create a Virtual Environment <br/>
Creating a virtual environment helps to manage dependencies for your project. Run the following command to create a virtual environment named authenv: <br/>

```bash
mkvirtualenv authenv

<br/>
# 2. Activate the Virtual Environment <br/>
activate the newly created virtual environment <br/>
```bash
source authenv/bin/activate

<br/>
# 3. Install Required Packages <br/>
Once the virtual environment is activated, install the necessary packages listed in requirements.txt: <br/>

```bash
pip install -r requirements.txt

<br/>
# 4. Apply Migrations
Before running the server, apply the migrations to set up your database schema: <br/>

```bash
python manage.py makemigrations
python manage.py migrate

<br/>
# 5. Run the Development Server
Start the Django development server to serve your application: <br/>

```bash
python manage.py runserver


## Requirements
<br/>
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
