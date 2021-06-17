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
    active = request.args.get('active')
    if active is not None:
        competition = Competition.query.filter(Competition.active == active).all()
    else:
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
    # if gender_id is None:
    #     return jsonify({"message": "Missing gender_id parameter"}), 400

    if gender_id is not None:

        # Gender filter
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
                    if 'has_maxscore' in event and event['has_maxscore'] == True:
                        if event['max_score'] is not None:
                            score.update(
                                {'result_ordoned': event['max_score'] + (event['max_score'] - score['result'])})
                    else:
                            score.update({'result_ordoned': score['result']})
                    event['scores'].append(score)

            # Order by event category (1 best) (max lowest)
            # Order scores by event by time
            # Order scores by event by score (result ordoned)
            # Order by tiebreak
            if 'has_maxscore' in event and event['has_maxscore'] == True:
                event['scores'].sort(
                    key=lambda p: (p['category']['position'], p['time'], p['result_ordoned'], p['tiebreak']))
            else:
                event['scores'].sort(
                    key=lambda p: (p['category']['position'], p['time'], p['result_ordoned'], p['tiebreak']))

            # Affect points (best = 1) to (latest = highest number)
            i = 0
            same_score_amount = 0
            for index, score in enumerate(event['scores']):
                if index > 0:  # means it's not the first one
                    if (score['category']['position'] == event['scores'][index - 1]['category']['position'] and
                            score['time'] == event['scores'][index - 1]['time'] and
                            score['result_ordoned'] == event['scores'][index - 1]['result_ordoned'] and
                            score['tiebreak'] == event['scores'][index - 1]['tiebreak']
                    ):  # Same category position, means same category
                        score['point'] = i
                        same_score_amount = same_score_amount + 1
                    else:
                        i = i + 1 + same_score_amount
                        same_score_amount = 0
                        score['point'] = i
                else:
                    i = i + 1 + same_score_amount
                    same_score_amount = 0
                    score['point'] = i
            # Storing the last code to use later for when a participant
            event['last_score'] = i + same_score_amount
        o = []
        # Affect scores to each competitors in competition.competitors
        competitors_result_dict = list()
        if 'competitors' in competition_dict and isinstance(competition_dict['competitors'], list):
            for competitor in competition_dict['competitors']:
                if competitor['gender']['id'] == gender_id:
                    competitor['scores'] = list()
                    total_competitor = 0
                    for event in events_list:
                        score_found_for_current_event = False
                        for score in event['scores']:
                            if score['competitor']['id'] == competitor['id']:
                                score_found_for_current_event = True
                                competitor['scores'].append(score)
                                total_competitor = total_competitor + score['point']
                        if score_found_for_current_event == False:
                            if 'last_score' in event and event['last_score'] > 0:
                                sc = dict()
                                sc['point'] = event['last_score'] + 1
                                sc['not_participated'] = True
                                sc['event'] = dict()
                                sc['event']['id'] = event['id']
                                sc['category'] = dict()

                                competitor['scores'].append(sc)
                                total_competitor = total_competitor + sc['point']
                    competitor['total_points'] = total_competitor
                    competitors_result_dict.append(competitor)
        # Set a rank on the competitor by summing all points in each event
        competitors_result_dict.sort(key=lambda p: (p['total_points']))
        rank = 1
        for cptt in competitors_result_dict:
            cptt['rank'] = rank
            rank = rank + 1
        resp_object = {'code': 20000, 'data': {'items': competitors_result_dict}}
        return jsonify(resp_object), 200
    else:
        # Team
        scores = Score.query. \
            join(Score.event).join(Score.team).filter(Event.competition_id == id) \
            .order_by(Event.order.asc())

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
                    if 'has_maxscore' in event and event['has_maxscore'] == True:
                        if event['max_score'] is not None:
                            score.update(
                                {'result_ordoned': event['max_score'] + (event['max_score'] - score['result'])})
                    else:
                        if 'max_score_best' in event and event['max_score_best'] == True:
                            score.update({'result_ordoned': score['result'] * -1})
                        else:
                            score.update({'result_ordoned': score['result']})
                    event['scores'].append(score)

            # Order by event category (1 best) (max lowest)
            # Order scores by event by time
            # Order scores by event by score (result ordoned)
            # Order by tiebreak
            if 'has_maxscore' in event and event['has_maxscore'] == True:
                event['scores'].sort(
                    key=lambda p: (p['category']['position'], p['time'], p['result_ordoned'], p['tiebreak']))
            else:
                event['scores'].sort(
                    key=lambda p: (p['category']['position'], p['time'], p['result_ordoned'], p['tiebreak']))

            # Affect points (best = 1) to (latest = highest number)
            i = 0
            same_score_amount = 0
            for index, score in enumerate(event['scores']):
                if index > 0:  # means it's not the first one
                    if (score['category']['position'] == event['scores'][index - 1]['category']['position'] and
                            score['time'] == event['scores'][index - 1]['time'] and
                            score['result_ordoned'] == event['scores'][index - 1]['result_ordoned'] and
                            score['tiebreak'] == event['scores'][index - 1]['tiebreak']
                    ):  # Same category position, means same category
                        score['point'] = i
                        same_score_amount = same_score_amount + 1
                    else:
                        i = i + 1 + same_score_amount
                        same_score_amount = 0
                        score['point'] = i
                else:
                    i = i + 1 + same_score_amount
                    same_score_amount = 0
                    score['point'] = i
            # Storing the last code to use later for when a participant
            event['last_score'] = i + same_score_amount
        o = []
        # Affect scores to each competitors in competition.teams
        teams_result_dict = list()
        if 'teams' in competition_dict and isinstance(competition_dict['teams'], list):
            for team in competition_dict['teams']:
                # if competitor['gender']['id'] == gender_id:
                team['scores'] = list()
                total_team = 0
                for event in events_list:
                    score_found_for_current_event = False
                    for score in event['scores']:
                        if score['team']['id'] == team['id']:
                            score_found_for_current_event = True
                            team['scores'].append(score)
                            total_team = total_team + score['point']
                    if score_found_for_current_event == False:
                        if 'last_score' in event and event['last_score'] > 0:
                            sc = dict()
                            sc['point'] = event['last_score'] + 1
                            sc['not_participated'] = True
                            sc['event'] = dict()
                            sc['event']['id'] = event['id']
                            sc['category'] = dict()

                            team['scores'].append(sc)
                            total_team = total_team + sc['point']
                team['total_points'] = total_team
                teams_result_dict.append(team)

        # Set a rank on the competitor by summing all points in each event
        teams_result_dict.sort(key=lambda p: (p['total_points']))
        rank = 1
        for cptt in teams_result_dict:
            cptt['rank'] = rank
            rank = rank + 1
        resp_object = {'code': 20000, 'data': {'items': teams_result_dict}}
        return jsonify(resp_object), 200
    return jsonify({'error':'error'}), 400

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

@app.route('/api/competition/team/add', methods=['POST'])
@jwt_required()
@cross_origin()
def add_team_to_competition():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}), 400
    team = request.json.get('team', None)
    competition = request.json.get('competition', None)
    if not team:
        return jsonify({"message": "Missing team parameter"}), 400
    if not competition:
        return jsonify({"message": "Missing competition parameter"}), 400
    linkCompetitionTeam = LinkCompetitionTeam()
    linkCompetitionTeam.competition_id = competition['id']
    linkCompetitionTeam.team_id = team['id']
    try:
        db.session.add(linkCompetitionTeam)
        db.session.flush()
        db.session.commit()
    except:
        db.session.rollback()
    resp_object = {'code': 20000, 'data': {'link_competition_team': None}}
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