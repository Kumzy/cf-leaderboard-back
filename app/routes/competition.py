from app import app, db
from flask import jsonify, request
from flask_cors import cross_origin
from app.models.competition import Competition, CompetitionSchema
import json
from app.models.link_competition_competitor import LinkCompetitionCompetitor
import decimal, datetime
from sqlalchemy.sql.expression import and_
from flask_jwt_extended import jwt_required
from app.models.score import Score, ScoreSchema
from app.models.event import Event, EventSchema
from app.models.competitor import Competitor
import operator

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
    # Get the leaderboard or 404
    competition = Competition.query.get_or_404(id)
    competition_schema = CompetitionSchema()
    competition_dict = competition_schema.dump(competition)
    # Retrieve gender first
    gender_id = request.args.get('gender_id')
    if gender_id is None:
        return jsonify({"message": "Missing gender_id parameter"}), 400

    scores = Score.query. \
        join(Score.event).join(Score.competitor).filter(Event.competition_id == id) \
        .filter(Competitor.gender_id == gender_id).order_by(Event.order.asc())
    score_schema = ScoreSchema(many=True)
    score_list = score_schema.dump(scores)

    # Get individual events
    events = Event.query.filter(Event.competition_id == id)
    event_schema = EventSchema(many=True)
    events_list = event_schema.dump(events)

    # Check that events is not empty
    # TODO: Check that events is not empty

    # Generate array of scores for each events
    for event in events_list:
        event['scores'] = list()
        for score in score_list:
            if score['event']['id'] == event['id']:
                if event['max_score'] is not None:
                    score.update({'result_ordoned': event['max_score'] + (event['max_score'] - score['result'])})
                event['scores'].append(score)

        # Order by event category (1 best) (max lowest)
        # Order scores by event by time
        # Order scores by event by score (result ordoned)
        # Order by tiebreak
        event['scores'].sort(key=lambda p: (p['category']['position'],p['time'],p['result_ordoned'],p['tiebreak']))

        # Affect points (best = 1) to (latest = highest number)
        i = 1
        for score in event['scores']:
            score['point'] = i
            i = i + 1
    o = []
    # Affect scores to each competitors in competition.competitors
    if 'competitors' in competition_dict and isinstance(competition_dict['competitors'],list):
        for competitor in competition_dict['competitors']:
            competitor['scores'] = list()
            # total_competitor = 0
            for event in events_list:
                for score in event['score']:
                    if score['competitor']['id'] == competitor['id']:
                        competitor['scores'].append(score)

    # Set a rank on the competitor by summing all points in each event


    resp_object = {'code': 20000, 'data': {'item': score_list}}
    return jsonify(resp_object), 200

@app.route('/api/competition', methods=['POST'])
@cross_origin()
@jwt_required()
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
@jwt_required()
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
@jwt_required()
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