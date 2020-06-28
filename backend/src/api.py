import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
import sys

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES

'''
Public end point to get all drink with short details
'''


@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.short() for drink in drinks]
    })


'''
Only user with permission 'get:drinks-detail' can access this end point
to get all drink with long details
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_details(token):
    drinks = Drink.query.all()
    return jsonify({
        "success": True,
        "drinks": [drink.long() for drink in drinks]
    })


'''
Only user with permission 'post:drinks' can access this end point
to create new drink
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(token):
    body = request.get_json()
    is_valid_body = is_valid_drink_body_on_create(body)

    if not is_valid_body:
        abort(400)

    req_title = body.get('title')
    req_recipes = body.get('recipe')

    # Check if the title is already exist
    validate_title_uniqueness(req_title)

    try:
        drink = Drink(title=req_title, recipe=json.dumps(req_recipes))
        drink.insert()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except:
        print(sys.exc_info())
        abort(422)


'''
Only user with permission 'patch:drinks' can access this end point
to update existing drink
'''


@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(token, drink_id):
    drink = Drink.query \
            .filter_by(id=drink_id) \
            .one_or_none()

    if drink is None:
        abort(404)

    body = request.get_json()
    req_title = body.get('title', None)
    req_recipes = body.get('recipe', None)

    # Check if the title is already exist
    validate_title_uniqueness(req_title)

    try:
        if req_title is not None:
            drink.title = req_title
        if req_recipes is not None:
            drink.recipe = json.dumps(req_recipes)
        drink.update()

        return jsonify({
            "success": True,
            "drinks": [drink.long()]
        })
    except:
        print(sys.exc_info())
        abort(422)


'''
Only user with permission 'patch:drinks' can access this end point
to delete existing drink
'''


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(token, drink_id):
    drink = Drink.query \
            .filter_by(id=drink_id) \
            .one_or_none()

    if drink is None:
        abort(404)

    try:
        drink.delete()

        return jsonify({
            "success": True,
            "delete": drink_id
        })
    except:
        abort(422)


# Helper Fucntions

def is_valid_drink_body_on_create(body):
    req_title = body.get('title', None)
    req_recipes = body.get('recipe', None)

    if req_title is None or req_recipes is None:
        return False

    if type(req_recipes) is list:
        for recipe in req_recipes:
            if 'name' not in recipe \
                    and 'color' not in recipe \
                    and 'parts' not in recipe:
                return False
    else:
        if 'name' not in recipe \
                and 'color' not in recipe \
                and 'parts' not in recipe:
            return False

    return True


def validate_title_uniqueness(title):
    drinks = Drink.query.filter_by(title=title).all()
    if len(drinks) > 0:
        abort(409)

# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(409)
def conflict(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": "rosource is already exist"
    }), 409


@app.errorhandler(401)
def not_authorize(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unathurize user"
    }), 401


@app.errorhandler(403)
def insufficient_permission(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "insufficient permission"
    }), 403
