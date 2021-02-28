import pandas as pd
from app import db

engine = db.get_engine()  # db is the one from the question
csv_gender_path = 'genders.csv'
csv_country_path = 'countries.csv'
csv_competitors_path = 'competitors.csv'

# Genders
# Read CSV with Pandas
with open(csv_gender_path, 'r', encoding='utf_8') as file:
    df_gender = pd.read_csv(file)

# Insert into DB
df_gender.to_sql('gender',
          con=engine,
          index=False,
          if_exists='append')

# Countries
# Read CSV with Pandas
with open(csv_country_path, 'r', encoding='utf_8') as file:
    df_country = pd.read_csv(file)

# Insert into DB
df_country.to_sql('country',
          con=engine,
          index=False,
          if_exists='append')


with open(csv_competitors_path, 'r', encoding='utf_8') as file:
    df_competitors = pd.read_csv(file)

for index, row in df_competitors.iterrows():
    db.session.execute("INSERT INTO competitor (firstname, lastname, weight, height, gender_id, nationality_id, birthday_date) values (:firstname,:lastname,:weight,:height,(select id from gender where name=:gender_name),(select id from country where name=:country_name),:birthday_date)",
                       {
                           "firstname":row.firstname,
                           "lastname": row.lastname,
                           "weight": row.weight,
                           "height": row.height,
                           "gender_name":row.gender,
                           "country_name":row.nationality,
                           "birthday_date":row.birthday_date
                       })

db.session.commit()