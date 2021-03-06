from app import app, db
from flask import jsonify, request
from flask_cors import cross_origin
from app.models.competitor import Competitor, CompetitorSchema
from app.models.link_competition_competitor import LinkCompetitionCompetitor

@app.route('/api/competitors', methods=['GET'])
@cross_origin()
def competitors():
    exclude_competitors_in_competition_id = request.headers.get('exclude_competitors_in_competition_id')
    if exclude_competitors_in_competition_id is not None:
        # Means we want only competitors that are not in the competition
        subquery = db.session.query(Competitor.id) \
                        .filter(Competitor.id == LinkCompetitionCompetitor.competitor_id) \
                        .filter(LinkCompetitionCompetitor.competition_id == exclude_competitors_in_competition_id)
        competitors = Competitor.query.filter(~Competitor.id.in_(subquery))
    else:
        competitors = Competitor.query.all()
    competitor_schema = CompetitorSchema(many=True)
    # Serialize the queryset
    result = competitor_schema.dump(competitors)
    resp_object = {'code': 20000, 'data': {'items': result}}
    return jsonify(resp_object), 200

@app.route('/api/competitor/<id>', methods=['GET'])
@cross_origin()
def competitor(id):
    competitor = Competitor.query.get_or_404(id)
    competitor_schema = CompetitorSchema(many=False)
    # Serialize the queryset
    result = competitor_schema.dump(competitor)
    resp_object = {'code': 20000, 'data': {'item': result}}
    return jsonify(resp_object), 200

@app.route('/api/competitor/<id>', methods=['PUT','DELETE'])
@cross_origin()
def competitor_protected(id):
    #TODO: Add protected to this route
    if request.method == 'DELETE':
        competitor = Competitor.query.get_or_404(id)
        db.session.delete(competitor)
        db.session.commit()
        competitor_schema = CompetitorSchema(many=False)
        # Serialize the queryset
        result = competitor_schema.dump(competitor)
        resp_object = {'code': 20000, 'data': {'item': result}}
        return jsonify(resp_object), 200
    elif request.method == 'PATCH':
        pass