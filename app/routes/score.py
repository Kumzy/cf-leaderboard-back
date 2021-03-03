from app import app, db
from flask import jsonify, request
from flask_cors import cross_origin
from app.models.score import Score, ScoreSchema

@app.route('/api/score', methods=['POST'])
@cross_origin()
def post_score():
    # if not request.is_json:
    #     return jsonify({"message": "Missing JSON in request"}), 400
    # name = request.json.get('name', None)
    # date_start = request.json.get('date_start', None)
    # if not name:
    #     return jsonify({"message": "Missing name parameter"}), 400
    # if not date_start:
    #     return jsonify({"message": "Missing date_start parameter"}), 400
    # competition = Score()
    # competition.name = name
    # competition.date_start = date_start
    # try:
    #     db.session.add(competition)
    #     db.session.flush()
    #     db.session.commit()
    # except:
    #     db.session.rollback()
    resp_object = {'code': 20000, 'data': {'competition': None}}
    return jsonify(resp_object), 200