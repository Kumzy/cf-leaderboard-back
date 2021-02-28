from app import app
from flask import jsonify
from flask_cors import cross_origin
from app.models.country import Country, CountrySchema

@app.route('/api/countries', methods=['GET'])
@cross_origin()
def countries():
    countries = Country.query.all()
    country_schema = CountrySchema(many=True)
    # Serialize the queryset
    result = country_schema.dump(countries)
    resp_object = {'code': 20000, 'data': {'items': result}}
    return jsonify(resp_object), 200