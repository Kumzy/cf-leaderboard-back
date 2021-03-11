from app import app, db
from flask import jsonify, request
from flask_cors import cross_origin
from app.models.competition import Competition, CompetitionSchema
import json
from app.models.link_competition_competitor import LinkCompetitionCompetitor
import decimal, datetime
from sqlalchemy.sql.expression import and_

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

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

@app.route('/api/competition/<id>/leaderboard', methods=['GET'])
@cross_origin()
def competition_leaderboard(id):
    # Retrieve gender first
    gender_id = request.args.get('gender_id')
    if gender_id is None:
        return jsonify({"message": "Missing gender_id parameter"}), 400
    sql_request = "with scores as ( " \
        "select competitor.id as competitor_id, " \
	    "to_jsonb(competitor.*) as competitor, " \
        "score.result, "\
        "to_jsonb(category.*) as category, "\
        "to_jsonb(event.*) as event, "\
        "event.id as event_id, "\
        "CASE WHEN event.max_score_best THEN ROW_NUMBER () OVER (PARTITION BY category.id,event.id ORDER BY score desc) + (category.position * 1000) "\
        "ELSE ROW_NUMBER () OVER (PARTITION BY category.id,event.id ORDER BY score) + (category.position * 1000) "\
        "END as position_wod " \
        "from score " \
        "left join event on score.event_id = event.id " \
        "left join category on category.id = score.category_id "\
        "left join competition on competition.id = event.competition_id "\
        "left join competitor on competitor.id = score.competitor_id "\
        "left join gender on gender.id = competitor.gender_id "\
        "where gender.id = :gender_id " \
        "and competition.id = :competition_id " \
        "order by event.name asc,  position asc "\
        "),scores_points as ( "\
        "SELECT *, "\
        "ROW_NUMBER () OVER (PARTITION BY event_id ORDER BY position_wod) as point "\
        "FROM scores) "\
        "select competitor.id, concat(competitor.firstname, ' ', competitor.lastname) as longname,  sum(scores_points.point) as points, jsonb_agg(scores_points.*) as events, "\
        "ROW_NUMBER () OVER (order by sum(scores_points.point) asc) as rank " \
        "from competitor " \
        "left join scores_points on scores_points.competitor_id = competitor.id " \
        "LEFT JOIN link_competition_competitor lcc on lcc.competitor_id = competitor.id " \
        "left join gender on gender.id = competitor.gender_id " \
        "where lcc.competition_id = :competition_id " \
        "and gender.id = :gender_id " \
        "group by competitor.id; "
    results = db.session.execute(
        sql_request,
        {'gender_id': gender_id, 'competition_id': id}
    )
    o = json.dumps([dict(r) for r in results], default=alchemyencoder)
    resp_object = {'code': 20000, 'data': {'items': json.loads(o)}}
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

@app.route('/api/competition/competitor/add', methods=['POST'])
@cross_origin()
def add_competitor_to_competition():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    competitor = request.json.get('competitor', None)
    competition = request.json.get('competition', None)
    if not competitor:
        return jsonify({"message": "Missing competitor parameter"}), 400
    if not competition:
        return jsonify({"message": "Missing competition parameter"}), 400
    linkCompetitionCompetitor = LinkCompetitionCompetitor()
    linkCompetitionCompetitor.competition_id = competition['id']
    linkCompetitionCompetitor.competitor_id = competitor['id']
    try:
        db.session.add(linkCompetitionCompetitor)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
    resp_object = {'code': 20000, 'data': {'link_competition_competitor': None}}
    return jsonify(resp_object), 200

@app.route('/api/competition/competitor', methods=['DELETE'])
@cross_origin()
def remove_competitor_from_competition():
    competitor_id = request.args.get('competitor_id')
    competition_id = request.args.get('competition_id')
    if not competition_id:
        return jsonify({"message": "Missing competition_id parameter"}), 400
    if not competitor_id:
        return jsonify({"message": "Missing competitor_id parameter"}), 400

    # linkCompetitionCompetitor = LinkCompetitionCompetitor()
    try:
        LinkCompetitionCompetitor.query.filter(and_(LinkCompetitionCompetitor.competitor_id == competitor_id,
                                                      LinkCompetitionCompetitor.competition_id == competition_id)).delete()
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "Error removing the competitor"}), 400
    resp_object = {'code': 20000, 'data': {'link_competition_competitor': None}}
    return jsonify(resp_object), 200