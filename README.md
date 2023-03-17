![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![Django Rest Framework](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Swagger](https://img.shields.io/badge/-Swagger-%23Clojure?style=for-the-badge&logo=swagger&logoColor=white)

# A Placement Management System

This simple web application assists users sync with the placement preparation process with various features it has. Contains API for user authentication, adding companies to prepare for, interviews and upload resumes.

http://localhost:8000/api-docs/

The API docs can be viewed using the above link. Swagger is used to generate API docs under the hood using a package called 'drf_spectacular'.

## Getting Started

* Create a new virtual environment and install packages specified in the requirements.txt file.

* Hook in your database of choice, make necessary database changes in the settings.py file inside the project folder. Obviously, some familiarity with Django folder structures is required for this. By default this project uses MySQL as database.

* Make migrations when you're done with the database settings and migrate.
* Run python manage.py runserver, and the application should be running on port 8000 by default.


## Built With


* [Python Django](https://www.djangoproject.com/)
* [Django Rest Framework](https://www.django-rest-framework.org/)
* [Swagger Docs](https://swagger.io/)

## Features 

Application aims to help professionals/students to keep track of interview preparation for companies. They can login, add questions, 
interview dates, applications of companies to target, resume uploading and more features are included in the app for the time being.

## Updates

<b>-11/3/23</b>

Vesco template added, since this is not a full fledged attempt to experiment with CSS, I decided to pick an old theme and integrate it into this Django app. Integration is not always easy, sometimes have to make a lot of adjustments with CSS and JS imports to make those compatible with a Django app.

<b>-17/3/23</b>

Removed the template added previously. For now, I plan to only have APIs for it with no multi-page front-end.

## Authors

* **Amit Prafulla (APFirebolt)** - (http://apgiiit.com/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Screenshots

No screenshots as of now, would be added in the future.

