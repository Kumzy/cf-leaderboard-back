from app import app
from flask import jsonify
from flask_cors import cross_origin
from app.models.competitor import Competitor, CompetitorSchema

@app.route('/api/competitors', methods=['GET'])
@cross_origin()
def competitors():
    competitors = Competitor.query.all()
    competitor_schema = CompetitorSchema(many=True)
    # Serialize the queryset
    result = competitor_schema.dump(competitors)
    resp_object = {'code': 20000, 'data': {'items': result}}
    return jsonify(resp_object), 200

@app.route('/api/competitor/<id>', methods=['GET','PUT'])
@cross_origin()
def competitor(id):
    competitor = Competitor.query.get_or_404(id)
    competitor_schema = CompetitorSchema(many=False)
    # Serialize the queryset
    result = competitor_schema.dump(competitor)
    resp_object = {'code': 20000, 'data': {'item': result}}
    return jsonify(resp_object), 200