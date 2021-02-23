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