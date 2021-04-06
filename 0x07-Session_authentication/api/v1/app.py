#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
import api.v1.views.users


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = None
if getenv('AUTH_TYPE') == 'auth':
    from api.v1.auth.auth import Auth
    auth = Auth()
elif getenv('AUTH_TYPE') == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Request unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ User is authenticate but not allowed
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_req():
    """Filtering of each request
    """
    pat = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    if auth is None:
        return

    if not auth.require_auth(request.path, pat):
        return None

    """if auth.require_auth(request.path, pat) is None:
        return None"""

    if auth.authorization_header(request) is None:
        abort(401)

    if auth.current_user is None:
        abort(403)

    request.current_user = auth.current_user(request)
    if user_id == 'me' and request.current_user is None:
        abort(404)

    if user_id == 'me' and request.current_user is not None:
        return jsonify(User)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
