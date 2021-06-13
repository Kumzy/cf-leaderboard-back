from app import app, db
from flask import jsonify, request
from flask_cors import cross_origin
from app.models.team import Team, TeamSchema
from app.models.competitor import Competitor
from app.models.link_team_competitor import LinkTeamCompetitor
from flask_jwt_extended import jwt_required

# @app.route('/api/teams', methods=['GET'])
# @cross_origin()
# def teams():
#     exclude_competitors_in_competition_id = request.args.get('exclude_competitors_in_competition_id')
#     if exclude_competitors_in_competition_id is not None:
#         # Means we want only competitors that are not in the competition
#         subquery = db.session.query(Competitor.id) \
#                         .filter(Competitor.id == LinkCompetitionCompetitor.competitor_id) \
#                         .filter(LinkCompetitionCompetitor.competition_id == exclude_competitors_in_competition_id)
#         competitors = Competitor.query.filter(~Competitor.id.in_(subquery))
#     else:
#         competitors = Competitor.query.all()
#     competitor_schema = CompetitorSchema(many=True)
#     # Serialize the queryset
#     result = competitor_schema.dump(competitors)
#     resp_object = {'code': 20000, 'data': {'items': result}}
#     return jsonify(resp_object), 200

# @app.route('/api/competitor/<id>', methods=['GET'])
# @cross_origin()
# def competitor(id):
#     competitor = Competitor.query.get_or_404(id)
#     competitor_schema = CompetitorSchema(many=False)
#     # Serialize the queryset
#     result = competitor_schema.dump(competitor)
#     resp_object = {'code': 20000, 'data': {'item': result}}
#     return jsonify(resp_object), 200
#
# @app.route('/api/competitor/<id>', methods=['PUT','DELETE'])
# @cross_origin()
# @jwt_required()
# def competitor_protected(id):
#     if request.method == 'DELETE':
#         competitor = Competitor.query.get_or_404(id)
#         db.session.delete(competitor)
#         db.session.commit()
#         competitor_schema = CompetitorSchema(many=False)
#         # Serialize the queryset
#         result = competitor_schema.dump(competitor)
#         resp_object = {'code': 20000, 'data': {'item': result}}
#         return jsonify(resp_object), 200
#     elif request.method == 'PUT':
#         if not request.is_json:
#             return jsonify({"message": "Missing JSON in request"}), 400
#         firstname = request.json.get('firstname', None)
#         lastname = request.json.get('lastname', None)
#         birthday_date = request.json.get('birthday_date', None)
#         height = request.json.get('height', None)
#         weight = request.json.get('weight', None)
#         gender = request.json.get('gender', None)
#         nationality = request.json.get('nationality', None)
#         avatar = request.json.get('avatar', None)
#         if not firstname:
#             return jsonify({"message": "Missing firstname parameter"}), 400
#         if not lastname:
#             return jsonify({"message": "Missing lastname parameter"}), 400
#         if not gender:
#             return jsonify({"message": "Missing gender parameter"}), 400
#         competitor = Competitor.query.get_or_404(id)
#         competitor.firstname = firstname
#         competitor.lastname = lastname
#         competitor.birthday_date = birthday_date
#         competitor.height = height
#         competitor.weight = weight
#         competitor.gender_id = gender['id']
#         competitor.nationality_id = nationality['id']
#         competitor.avatar = avatar
#         try:
#             db.session.add(competitor)
#             db.session.commit()
#         except:
#             db.session.rollback()
#             return jsonify({"message": "Error updating"}), 400
#         resp_object = {'code': 20000, 'data': {'competitor': None}}
#         return jsonify(resp_object), 200

@app.route('/api/team', methods=['POST'])
@jwt_required()
@cross_origin()
def team_post():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    name = request.json.get('name', None)
    competitor_1 = request.json.get('competitor_1', None)
    competitor_2 = request.json.get('competitor_2', None)
    competition = request.json.get('competition', None)
    if not name:
        return jsonify({"message": "Missing name parameter"}), 400
    if not competitor_1 and not 'id' in competitor_1:
        return jsonify({"message": "Missing competitor 1 parameter"}), 400
    if not competitor_2 and not 'id' in competitor_2:
        return jsonify({"message": "Missing competitor 2 parameter"}), 400
    if not competition and not 'id' in competition:
        return jsonify({"message": "Missing competition parameter"}), 400
    team = Team()
    team.name = name
    team.competition_id = competition['id']
    try:
        db.session.add(team)
        ltc1 = LinkTeamCompetitor()
        ltc1.competitor_id = competitor_1['id']
        ltc2 = LinkTeamCompetitor()
        ltc2.competitor_id = competitor_2['id']
        db.session.flush()
        ltc1.team_id = team.id
        ltc2.team_id = team.id
        db.session.add(ltc1)
        db.session.add(ltc2)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "Error inserting"}), 400
    resp_object = {'code': 20000, 'data': {'team': None}}
    return jsonify(resp_object), 200
