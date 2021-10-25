<!-- PROJECT INFO -->
<h1 align="center">
  <br>
  Message in a Bottle Backend API
  <br>
</h1>

<h4 align="center">RESTful API for Message in a Bottle frontend application consumption.</h4>

<p align="center">
  <a href="https://github.com/marlitas/rails_engine/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/MIBFB-COLLAB/message_in_a_bottle_backend?style=for-the-badge" alt="contributors_badge">
  </a>
  <a href="https://github.com/marlitas/rails_engine/network/members">
    <img src="https://img.shields.io/github/forks/MIBFB-COLLAB/message_in_a_bottle_backend?style=for-the-badge" alt="forks_badge">
  </a>
  <a href="https://github.com/marlitas/rails_engine/stargazers">
    <img src="https://img.shields.io/github/stars/MIBFB-COLLAB/message_in_a_bottle_backend?style=for-the-badge" alt="stars_badge">
  </a>
  <a href="https://github.com/marlitas/rails_engine/issues">
    <img src="https://img.shields.io/github/issues/MIBFB-COLLAB/message_in_a_bottle_backend?style=for-the-badge" alt="issues_badge">


<!-- CONTENTS -->
<p align="center">
  <a href="#about-the-project">About The Project</a> •
  <a href="#tools-used">Tools Used</a> •
  <a href="#set-up">Set Up</a> •
  <a href="#installation">Installation</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#database-schema">Database Schema</a> •
  <a href="#contributing">Contributing</a> •
  <a href="#acknowledgements">Acknowledgements</a>
</p>



## About The Project

Message in a Bottle is an application where users can discover stories about the communities around them. This app was designed as a way to interact with cities, neighborhoods, and the people that inhabit them. The Message in a Bottle backend is built with a Django framework that stores story and user data through PostgreSQL. We expose this data to our frontend team to build out the user interface.

### Learning Goals

* Building a RESTful API with a Django/Python backend
* Collaborating with a Front End team
* Geolocation calls and tracking
* Python TDD practices


## Tools Used

| Development | Testing       | Packages              |
|   :----:    |    :----:     |    :----:             |
| Python 3.9.7| Pytest Django | Django                |
| Django      | Pytest-Cov    | Django CORS Headers   |
| CircleCI    | Postman       | Django Heroku         |
| PostgreSQL  |               | Django REST Framework |
| Git/Github  |               | Gunicorn              |
| Heroku      |               | Psycopg2              |
|             |               | Pycodestyle           |
|             |               | Python-Decouple       |
|             |               | Python-DotENV         |
|             |               | Requests              |


## Set Up

1. To clone and run this application, you'll need Python 3.8.2 and Django. Using [rbenv](https://github.com/rbenv/rbenv) you can install Ruby 2.7.2 (if you don't have it already) with:
```sh
rbenv install 2.7.2
```
2. With rbenv you can set up your Ruby version for a directory and all subdirectories within it. Change into a directory that will eventually contain this repo and then run:
```sh
rbenv local 2.7.2
```
You can check that your Ruby version is correct with `ruby -v`

3. Once you have verified your Ruby version is 2.7.2, check if you have Rails. From the command line:
```sh
rails -v
```
4. If you get a message saying rails is not installed or you do not have version 5.2.5, run
```sh
gem install rails --version 5.2.5
```
5. You may need to quit and restart your terminal session to see these changes show up



## Run Locally

1. Fork this repo
2. Clone your new repo
   ```sh
   git clone https://github.com/MIBFB-COLLAB/message_in_a_bottle_backend.git
   ```
3. Create and Invoke your virtual environment
  ```sh
  python3 -m virtualenv venv

  source <virtual env>/bin/activate
  ```
4. Install dependencies
   ```sh
   python -m pip install -r requirements.txt
   ```
5. Setup the database
  ```sh
  psql

  CREATE DATABASE <project name>;

  CREATE USER <user name> WITH PASSWORD <password>;

  ALTER ROLE myprojectuser SET client_encoding TO 'utf8';
  ALTER ROLE myprojectuser SET default_transaction_isolation TO 'read committed';
  ALTER ROLE myprojectuser SET timezone TO 'UTC';

  GRANT ALL PRIVILEGES ON DATABASE <project name TO <user name>;

  ```
6. Add PostgreSQL database info to settings.py file

7. python manage.py migrate


## How To Use

To experience the UI our frontend team built please [visit](link). Otherwise you may hit our endpoints through an http request helper such as Postman.



### Endpoint Documentation

Domain: 'https://message-in-a-bottle-api.herokuapp.com'

[Stories Index Endpoint](https://message-in-a-bottle-api.herokuapp.com/api/v1/stories)
<br>
The GET stories endpoint has two options for retrieving stories near you. You may either supply a City, State as a query param, or longitude and latitude.

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
        "distance_in_miles": 1.2
        }
      },
      {
      "id": 2,
      "type": "story",
      "attributes": {
        "title": "story",
        "latitude": 13.563,
        "longitude": 10.2673,
        "distance_in_miles": 3
        }
      }
    ]
  }
}
```

[Story Show Endpoint](https://message-in-a-bottle.herokuapp.com/api/v1/stories/166)
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
      "latitude": 13.201,
      "longitude": 9.2673,
      "distance_in_miles": 1.2
      }
   }
}
```

[Directions Endpoint](https://message-in-a-bottle.herokuapp.com/api/v1/stories/166/directions)
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
  "latitude": 123.92,
  "longitude": 29.758
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
      "latitude": 123.92,
      "longitude": 29.758
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
      "latitude": 1239.2,
      "longitude": 29.758
    }
  }
}
```

**Delete Story Endpoint**
<br>
Request:
DELETE `/api/v1/stories/:id`



## Database Schema
![MIAB DB Schema](https://user-images.githubusercontent.com/56685055/138749880-bccbafc1-3a32-43ac-8df3-5314dc65aa16.png)



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
