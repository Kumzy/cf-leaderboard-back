from app import app, db
from flask import jsonify, request
from flask_cors import cross_origin
from app.models.score import Score, ScoreSchema
from app.models.event import Event
from flask_jwt_extended import jwt_required

@app.route('/api/score', methods=['POST'])
@jwt_required()
@cross_origin()
def post_score():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    event = request.json.get('event', None)
    competitor = request.json.get('competitor', None)
    category = request.json.get('category', None)
    result = request.json.get('result', None)
    time = request.json.get('time', None)
    tiebreak = request.json.get('tiebreak', None)
    if not event:
        return jsonify({"message": "Missing event parameter"}), 400
    if not competitor:
        return jsonify({"message": "Missing competitor parameter"}), 400
    if not category:
        return jsonify({"message": "Missing category parameter"}), 400
    if not result:
        return jsonify({"message": "Missing result parameter"}), 400
    if not time:
        return jsonify({"message": "Missing time parameter"}), 400
    if not tiebreak:
        return jsonify({"message": "Missing tiebreak parameter"}), 400
    score = Score()
    score.event_id = event['id']
    score.competitor_id = competitor['id']
    score.category_id = category['id']
    score.result = result
    score.tiebreak = tiebreak
    score.time = time
    try:
        db.session.add(score)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "Could not insert data"}), 400
    resp_object = {'code': 20000, 'data': {'item': None}}
    return jsonify(resp_object), 200

@app.route('/api/score/<id>', methods=['PUT','DELETE'])
@cross_origin()
@jwt_required()
def edit_score(id):
    if request.method == 'DELETE':
        score = Score.query.get_or_404(id)
        db.session.delete(score)
        db.session.commit()
        score_schema = ScoreSchema(many=False)
        # Serialize the queryset
        result = score_schema.dump(score)
        resp_object = {'code': 20000, 'data': {'item': result}}
        return jsonify(resp_object), 200
    elif request.method == 'PUT':
        score = Score.query.get_or_404(id)
        if not request.is_json:
            return jsonify({"message": "Missing JSON in request"}), 400
        event = request.json.get('event', None)
        competitor = request.json.get('competitor', None)
        category = request.json.get('category', None)
        result = request.json.get('result', None)
        time = request.json.get('time', None)
        tiebreak = request.json.get('tiebreak', None)
        if not event:
            return jsonify({"message": "Missing event parameter"}), 400
        if not competitor:
            return jsonify({"message": "Missing competitor parameter"}), 400
        if not category:
            return jsonify({"message": "Missing category parameter"}), 400
        if not result:
            return jsonify({"message": "Missing result parameter"}), 400
        if not time:
            return jsonify({"message": "Missing time parameter"}), 400
        if not tiebreak:
            return jsonify({"message": "Missing tiebreak parameter"}), 400
        score.event_id = event['id']
        score.competitor_id = competitor['id']
        score.category_id = category['id']
        score.result = result
        score.tiebreak = tiebreak
        score.time = time
        try:
            db.session.add(score)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "Error updating"}), 400
        resp_object = {'code': 20000, 'data': {'score': None}}
        return jsonify(resp_object), 200

@app.route('/api/competition/<id>/scores', methods=['GET'])
@cross_origin()
def get_scores(id):
    scores = Score.query.join(Score.event).filter(Event.competition_id == id)
    score_schema = ScoreSchema(many=True)
    # Serialize the queryset
    result = score_schema.dump(scores)
    resp_object = {'code': 20000, 'data': {'items': result}}
    return jsonify(resp_object), 200