from app import app, db
from flask import jsonify, request
from flask_cors import cross_origin
from app.models.score import Score, ScoreSchema
from flask_jwt_extended import jwt_required

@app.route('/api/score', methods=['POST'])
# TODO: Add jwt_required for auth required to access this route
@jwt_required()
@cross_origin()
def post_score():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    event = request.json.get('event', None)
    competitor = request.json.get('competitor', None)
    category = request.json.get('category', None)
    result = request.json.get('result', None)
    if not event:
        return jsonify({"message": "Missing event parameter"}), 400
    if not competitor:
        return jsonify({"message": "Missing competitor parameter"}), 400
    if not category:
        return jsonify({"message": "Missing category parameter"}), 400
    if not result:
        return jsonify({"message": "Missing result parameter"}), 400
    score = Score()
    score.event_id = event['id']
    score.competitor_id = competitor['id']
    score.category_id = category['id']
    score.result = result
    try:
        db.session.add(score)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "Could not insert data"}), 400
    resp_object = {'code': 20000, 'data': {'item': None}}
    return jsonify(resp_object), 200