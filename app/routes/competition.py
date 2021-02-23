from app import app
from flask import jsonify
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
    resp_object = {'code': 20000, 'data': {'competition': result}}
    return jsonify(resp_object), 200