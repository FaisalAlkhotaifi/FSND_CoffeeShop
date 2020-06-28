# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "resource not found"
}
```
The API will return six error types when requests fail:
- 400: Bad Request
- 401: Unathurize User 
- 403: Insufficient Permission
- 404: Resource Not Found
- 409: Conflict
- 422: Not Processable

### Endpoints 

#### GET /drinks
- General:
    - Returns a list of drinks with limited info, success value
    - It is a public
- Sample: `curl http://127.0.0.1:5000/drinks`


#### GET /drinks-detail
- General:
    - Returns a list of drinks, success value
    - It accessed only by user with permission 'get:drinks-detail'
- Sample: `curl http://127.0.0.1:5000/drinks-detail`


#### POST /drinks
- General:
    - Including a body that contains title, recipe
    - Title should be unique
    - Recipe should in dictionary format which contains name, color, amd parts
    - Returns a list that contains only the new drink added and success value
    - It accessed only by user with permission 'post:drinks'
- Sample: `curl http://127.0.0.1:5000/drinks -X POST -H "Content-Type: application/json" -d '{ "id": -1, "recipe": [{ "color": "#cdf4fe", "name": "Blue Foam", "parts": 2 }, { "color": "#02b3e4", "name": "Blue Berry", "parts": 3 }], "title": "Udaci-Spice Latte" }'`


#### PATCH /drinks/<int:drink_id>
- General:
    - Including a body that contains optional title and recipe that needed to be updated
    - Title should be unique
    - Recipe should in dictionary format which contains name, color, amd parts
    - Returns a list that contains only the updated drink and success value
    - It accessed only by user with permission 'patch:drinks'
- Sample: `curl http://127.0.0.1:5000/drinks/1 -X PATCH -H "Content-Type: application/json" -d '{"title": "Udaci-Spice Latte" }'`


#### DELETE /drinks/<int:drink_id>
- General:
    - Returns a deleted drink id and success value
- Sample: `curl http://127.0.0.1:5000/drinks/1 -X DELETE`
