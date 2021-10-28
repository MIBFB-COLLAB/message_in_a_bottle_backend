<!-- PROJECT INFO -->
<h1 align="center">
  <br>
  Message in a Bottle Backend API
  <br>
</h1>

<h4 align="center">RESTful API for Message in a Bottle frontend application consumption.</h4>

<p align="center">
  <a href="https://github.com/marlitas/message_in_a_bottle_backend/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/MIBFB-COLLAB/message_in_a_bottle_backend?style=for-the-badge" alt="contributors_badge">
  </a>
  <a href="https://github.com/marlitas/message_in_a_bottle_backend/network/members">
    <img src="https://img.shields.io/github/forks/MIBFB-COLLAB/message_in_a_bottle_backend?style=for-the-badge" alt="forks_badge">
  </a>
  <a href="https://github.com/marlitas/message_in_a_bottle_backend/stargazers">
    <img src="https://img.shields.io/github/stars/MIBFB-COLLAB/message_in_a_bottle_backend?style=for-the-badge" alt="stars_badge">
  </a>
  <a href="https://github.com/marlitas/message_in_a_bottle_backend/issues">
    <img src="https://img.shields.io/github/issues/MIBFB-COLLAB/message_in_a_bottle_backend?style=for-the-badge" alt="issues_badge">
  <img src="https://img.shields.io/circleci/build/github/MIBFB-COLLAB/message_in_a_bottle_backend?style=for-the-badge">
  <img src="https://img.shields.io/badge/API_version-V1-or.svg?&style=for-the-badge&logoColor=white">


<!-- CONTENTS -->
<p align="center">
  <a href="#about-the-project">About The Project</a> •
  <a href="#tools-used">Tools Used</a> •
  <a href="#local-set-up">Local Set Up</a> •
  <a href="#installation">Installation</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#database-schema">Database Schema</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#acknowledgements">Acknowledgements</a>
</p>



## About The Project

Message in a Bottle is an application where users can discover stories about the communities around them. This app was designed as a way to interact with cities, neighborhoods, and the people that inhabit them. The Message in a Bottle backend is built with a Django framework that stores story and user data through PostgreSQL. We expose this data to our frontend team to build out the user interface.

### Learning Goals

* Building a RESTful API with a Python Django backend
* Collaborating with a Front-End dev team
* Geolocation calls and tracking
* Applying best practices learned during Turing to a new language and framework
  * e.g. TDD, OOP, REST, MVC(Rails) <--> MTV(Django)
* Making use of the `git rebase` workflow


## Tools Used

| Development | Testing       | Packages              |
|   :----:    |    :----:     |    :----:             |
| Python 3.9.7| Pytest-Django | Django                |
| Django      | Pytest-Cov    | Django CORS Headers   |
| CircleCI    | Postman       | Django Heroku         |
| PostgreSQL  | VCRPY         | Django REST Framework |
| Git/Github  |               | Gunicorn              |
| Heroku      |               | Psycopg2              |
|             |               | Pycodestyle           |
|             |               | Python-Decouple       |
|             |               | Python-DotENV         |
|             |               | Requests              |


## Local Set Up

1. To clone and run this application, you'll need Python 3.9.7 and Django 3.2.8. Using the official [Python docs](https://docs.python-guide.org/starting/installation/), follow instructions to install `python3` for your local OS.

2. You can check for a successful installation using this command:
```sh
$ python3 -V
> Python 3.9.7
```

## Installation

1. Fork this repo
2. Clone your new repo:
  ```sh
  git clone https://github.com/MIBFB-COLLAB/message_in_a_bottle_backend.git
  ```
3. Create and Invoke your virtual environment:
  ```sh
  python3 -m virtualenv venv
  source venv/bin/activate
  ```
4. Install dependencies:
  ```sh
  (venv) python -m pip install -r requirements.txt
  ```
5. Set up the database:
  ```sh
  $ psql

  CREATE DATABASE <project name>;
  CREATE USER <user name> WITH PASSWORD <password>;
  ALTER ROLE <user name> SET client_encoding TO 'utf8';
  ALTER ROLE <user name> SET default_transaction_isolation TO 'read committed';
  ALTER ROLE <user name> SET timezone TO 'UTC';
  GRANT ALL PRIVILEGES ON DATABASE <project name> TO <user name>;
  \q
  ```
6. Add PostgreSQL database info to `settings.py` file:
  ```python
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '<project name>',
        'USER': '<user name>',
        'PASSWORD': '<password>',
        'HOST': '<host>',
        'PORT': '<port>',
    }
  }
  ```

7. Migrate database:
  ```sh
  (venv) python manage.py makemigrations
  (venv) python manage.py migrate
  ```

8. Update CORS allowed origins in `settings.py`. Domains currently allowed are:
  ```python
  CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'https://message-in-a-bottle-fe-app.herokuapp.com',
    'https://app-message-in-a-bottle.herokuapp.com',
  ]
  ```

9. Run your local Python server with:
```sh
(venv) python manage.py runserver
```


## How To Use

To experience the front-end UI, please visit the application [here](https://message-in-a-bottle-fe-app.herokuapp.com/). You can also hit our endpoints through an API client, such as Postman or HTTPie.



### Endpoint Documentation

Domain: `https://message-in-a-bottle-api.herokuapp.com`

[Stories Index Endpoint](https://message-in-a-bottle-api.herokuapp.com/api/v1/stories?latitude=39.775506&longitude=-105.0066986)
<br>
The GET stories endpoint retrieves stories near you. You must supply valid `longitude` and `latitude` coordinates.

| Query Params | Required? | Example | Notes |
|   :----:     |   :----:  | :----:  | :----: |
| latitude     | Yes        | `/api/v1/stories?latitude=12.345&longitude=4.5968` | requires longitude |
| longitude    | Yes        | `/api/v1/stories?latitude=12.345&longitude=4.5968` | requires latitude |

Request:
GET `/api/v1/stories?latitude=12.3456&longitude=4.5968`

Response:
```json
{
  "data": {
    "input_location": "phoenix,az",
    "stories":[
      {
      "id": 1,
      "type": "story",
      "attributes": {
        "title": "my cool story",
        "latitude": 13.201,
        "longitude": 9.2673,
        "distance_in_miles": 1.2,
        "created_at": "2021-10-27T03:45:34.165600Z",
        "updated_at": "2021-10-27T03:45:36.855162Z"
        }
      },
      {
      "id": 2,
      "type": "story",
      "attributes": {
        "title": "story",
        "latitude": 13.563,
        "longitude": 10.2673,
        "distance_in_miles": 3,
        "created_at": "2021-10-27T04:45:34.165600Z",
        "updated_at": "2021-10-27T04:45:36.855162Z"
        }
      }
    ]
  }
}
```

[Story Show Endpoint](https://message-in-a-bottle-api.herokuapp.com/api/v1/stories/166?latitude=39.775506&longitude=-105.0066986)
<br>
    Request:
GET `/api/v1/stories/:id?latitude=12.3456&longitude=-4.5968`

Response:
```json
{
  "data": {
    "id": 1,
    "type": "story",
    "attributes": {
      "title": "my cool story",
      "message": "This one time I saw a bird",
      "name": "Anonymous",
      "created_at": "2021-10-08T23:28:51.897746Z",
      "updated_at": "2021-10-08T23:28:51.897746Z",
      "latitude": 30.071945143440377,,
      "longitude": 31.225164325479227,
      "distance_in_miles": 1.2,
      "location": "Cairo Governorate, EG"
      }
   }
}
```

[Directions Endpoint](https://message-in-a-bottle-api.herokuapp.com/api/v1/stories/166/directions?latitude=39.775506&longitude=-105.0066986)
<br>
Request:
GET `/api/v1/stories/:id/directions?latitude=1230&longitude=1209.3`

Response:
```json
{
  "data": [
    {
      "id": null,
      "type": "directions",
      "attributes": {
        "narrative": "Turn left on Bob St.",
        "distance": ".8 miles"
      }
    },
    {
      "id": null,
      "type": "directions",
      "attributes": {
        "narrative": "Turn right on Starry Road",
        "distance": ".2 miles"
      }
    }
  ]
}
```

**Create Story Endpoint**
<br>
Request:
POST `/api/v1/stories`

Request Body:
```json
{
  "title": "A new title",
  "message": "I'm coming up",
  "latitude": 27.717311514603534,
  "longitude": 85.32098499247293
}
```

Response:
```json
{
  "data": {
    "id": 2,
    "type": "story",
    "attributes": {
      "title": "A new title",
      "message": "I'm coming up",
      "name": "Anonymous",
      "created_at": "2021-10-08T23:28:51.897746Z",
      "updated_at": "2021-10-08T23:28:51.897746Z",
      "latitude": 27.717311514603534,
      "longitude": 85.32098499247293,
      "location": "Kathmandu, NP"
    }
  }
}
```

**Update Story Endpoint**
<br>
Request:
PATCH `/api/v1/stories/:id`

Request Body:
```json
{
  "title": "My Fixed Title",
  "message": "Hello World.",
  "name": "Sally"
}
```

Response:
```json
{
  "data": {
    "id": 1,
    "type": "story",
    "attributes": {
      "title": "My Fixed Title",
      "message": "Hello World.",
      "name": "Sally",
      "created_at": "2021-10-08T23:28:51.897746Z",
      "updated_at": "2021-10-18T23:28:51.897746Z",
      "latitude": 40.3830,
      "longitude": 105.5190,
      "location": "Estes Park, CO"
    }
  }
}
```

**Delete Story Endpoint**
<br>
Request:
DELETE `/api/v1/stories/:id`


**Error Handling**
<br>
Here are some examples of error messages you could receive if you send an invalid request:

Bad Request URI: GET `/api/v1/stories/:id` or `/api/v1/stories/:id?latitude=&longitude=`

Response:
```json
{
    "errors": {
        "messages": [
            "Latitude or longitude can't be blank."
        ],
        "code": 1
    }
}
```

Bad Request URI: GET `/api/v1/stories/:id?latitude=1000&longitude=1000`

Response:
```json
{
    "errors": {
        "messages": [
            "Invalid latitude or longitude."
        ],
        "code": 1
    }
}
```

Bad Request URI: GET `/api/v1/stories/:id?latitude=0&longitude=0`

Response:
```json
{
    "errors": {
        "messages": [
            "Impossible route."
        ],
        "code": 2
    }
}
```

POST `/api/v1/stories`
Bad Request Body:
```json
{
    "title":"Here's Johnny!",
    "message": "allworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboyallworkandnoplaymakesjackadullboy",
    "name":"Jack Torrance",
    "latitude":40.3830,
    "longitude":105.5190
}
```

Response:
```json
{
    "errors": {
        "message": [
            "Ensure this field has no more than 1000 characters."
        ],
        "location": [
            "This field may not be blank."
        ]
    }
}
```
    

## Database Schema
![Screen Shot 2021-10-27 at 17 33 14](https://user-images.githubusercontent.com/58891447/139162165-2312a560-e00c-43ab-9dfb-caadc0d8ad85.png)



## Contributing

👤  **Marla Schulz**
- [GitHub](https://github.com/marlitas)
- [LinkedIn](https://www.linkedin.com/in/marla-a-schulz/)

👤  **Taylor Varoglu**
- [GitHub](https://github.com/tvaroglu)
- [LinkedIn](https://www.linkedin.com/in/taylorvaroglu/)

👤  **Matt Kragen**
- [GitHub](https://github.com/matt-kragen)
- [LinkedIn](https://www.linkedin.com/in/mattkragen/)

👤  **Mae Duphorne**
- [GitHub](https://github.com/maeduphorne)
- [LinkedIn](https://www.linkedin.com/in/maeduphorne/)

👤  **Fara Akhatova**
- [GitHub](https://github.com/Fakhatova)
- [LinkedIn](https://www.linkedin.com/in/fara-akhatova/)

👤  **Justin Anthony**
- [GitHub](https://github.com/justincanthony)
- [LinkedIn](https://www.linkedin.com/in/justincanthony/)


## Acknowledgements

* [Turing School of Software and Design](https://turing.edu/)
  - Project created for completion towards Backend Engineering Program
* [MapQuest API](https://developer.mapquest.com/documentation/)
  - Radius Search, Route, and Reverse Geocoding APIs
