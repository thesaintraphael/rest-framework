# DRF App

App with JWT authentication, Class Based Views, Serializers, Swagger UI,
CI/CD and other cool DRF stuff

## API Documentaion

    /swagger - Swagger UI for API docs
    /swagger/api.json - JSON format of docs. Install or import to Postman
    /redoc- Read only doc.


## Run Locally
     1. Create virtual environment and activate it: 
            python -m venv venv
            venv\Scripts\activate
     
     2. Install requirements: 
            pip install -r requirements.txt
     
     3. Migrate db: 
            py manage.py migrate

     4. Run: 
            py manage.py runserver


## Executing Tests
     1. Runnning all tests: 
            python manage.py test
     
     2. Running only unittests (without db creation): 
            a. python manage.py unittest (custom command)
            b. python manage.py test --testrunner="unit_test_runner.UnitTestRunner"
