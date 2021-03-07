from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.models.user import User
from flask import jsonify
from flask_cors import cross_origin
from flask_jwt_extended import unset_jwt_cookies, create_access_token, get_jwt_identity, set_refresh_cookies, create_refresh_token, jwt_required, set_access_cookies

@app.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True) #Changed from jwt_refresh_token_required in 4.0.0
def refresh():
    # Create the new access token
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    # Set the access JWT and CSRF double submit protection cookies
    # in this response
    resp = jsonify({'refresh': True})
    set_access_cookies(resp, access_token)
    return resp, 200

@app.route('/token/login', methods=['POST'])
@cross_origin()
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not email:
        return jsonify({"message": "Missing email parameter"}), 400
    if not password:
        return jsonify({"message": "Missing password parameter"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User doesn't exist"}), 400
    if not user.check_password(password):
        return jsonify({"message": "Incorrect password"}), 401
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    # response_object = {'code': 20000, 'token': access_token}
    response_object = jsonify({'code': 20000, 'token': access_token})
    # set_access_cookies(response_object, access_token)
    # set_refresh_cookies(response_object, refresh_token)
    return response_object, 200

@app.route('/token/logout', methods=['POST'])
@cross_origin()
def logout():
    resp = {'code': 20000}
    # unset_jwt_cookies(resp)
    return jsonify(resp), 200

# @app.route('/register', methods=['POST'])
# @cross_origin()
# def register():
#     if not request.is_json:
#         return jsonify({"message": "Missing JSON in request"}), 400
#     email = request.json.get('email', None)
#     firstname = request.json.get('firstname', None)
#     lastname = request.json.get('lastname', None)
#     password = request.json.get('password', None)
#     if not email:
#         return jsonify({"message": "Missing email parameter"}), 400
#     if not password:
#         return jsonify({"message": "Missing password parameter"}), 400
#
#     user = User(firstname=firstname, lastname=lastname, email=email)
#     user.set_password(password)
#     db.session.add(user)
#     db.session.commit()
#     response_object = {'code': 20000}
#     return jsonify(response_object)

# @app.route('/api/user', methods=['GET'])
# @cross_origin()
# def user():
#     #current_user = get_jwt_identity()
#     #return jsonify(logged_in_as=current_user), 200
#     response_object = {'code': 20000, 'roles': ['admin'], 'name': 'Julien', 'introduction': 'yolo', 'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'}
#     return jsonify(response_object), 200