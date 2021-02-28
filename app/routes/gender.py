from app import app
from flask import jsonify
from flask_cors import cross_origin
from app.models.gender import Gender, GenderSchema

@app.route('/api/genders', methods=['GET'])
@cross_origin()
def genders():
    genders = Gender.query.all()
    gender_schema = GenderSchema(many=True)
    # Serialize the queryset
    result = gender_schema.dump(genders)
    resp_object = {'code': 20000, 'data': {'items': result}}
    return jsonify(resp_object), 200