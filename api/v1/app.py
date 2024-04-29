#!/usr/bin/python3
"""App"""
from api.v1.views import app_views
from flasgger import Swagger
from flasgger.utils import swag_from
from models import storage
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def close_db(error):
    """close"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """404 Error"""
    return make_response(jsonify({'error': "Not found"}), 404)

app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}

Swagger(app)


if __name__ == "__main__":
    """main"""
    p = environ.get('HBNB_API_PORT')
    h = environ.get('HBNB_API_HOST')
    if not p:
        p = '5000'
    if not h:
        h = '0.0.0.0'
    app.run(host=h, port=p, threaded=True)
