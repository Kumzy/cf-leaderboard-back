from app import app, db
from flask import jsonify, request
from flask_cors import cross_origin
from app.models.competition import Competition, CompetitionSchema

@app.route('/api/competitions', methods=['GET'])
@cross_origin()
def competitions():
    competition = Competition.query.all()
    competition_schema = CompetitionSchema(many=True)
    # Serialize the queryset
    result = competition_schema.dump(competition)
    resp_object = {'code': 20000, 'data': {'items': result}}
    return jsonify(resp_object), 200

@app.route('/api/competition/<id>', methods=['GET'])
@cross_origin()
def competition(id):
    competition = Competition.query.get_or_404(id)
    competition_schema = CompetitionSchema()
    # Serialize the queryset
    result = competition_schema.dump(competition)
    resp_object = {'code': 20000, 'data': {'item': result}}
    return jsonify(resp_object), 200

@app.route('/api/competition', methods=['POST'])
@cross_origin()
def post_competition():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    name = request.json.get('name', None)
    date_start = request.json.get('date_start', None)
    if not name:
        return jsonify({"message": "Missing name parameter"}), 400
    if not date_start:
        return jsonify({"message": "Missing date_start parameter"}), 400
    competition = Competition()
    competition.name = name
    competition.date_start = date_start
    try:
        db.session.add(competition)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
    resp_object = {'code': 20000, 'data': {'competition': None}}
    return jsonify(resp_object), 200