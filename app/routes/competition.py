from app import app
from flask import jsonify
from flask_cors import cross_origin
from app.models.competition import Competition, CompetitionSchema

@app.route('/api/competitions', methods=['GET'])
@cross_origin()
def competitors():
    competition = Competition.query.all()
    competition_schema = CompetitionSchema(many=True)
    # Serialize the queryset
    result = competition_schema.dump(competition)
    resp_object = {'code': 20000, 'data': {'items': result}}
    return jsonify(resp_object), 200