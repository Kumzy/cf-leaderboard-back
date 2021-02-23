class Config(object):

    POSTGRES = {
        'user': 'postgres',
        'pw': 'postgres',
        'db': 'cf_leaderboard',
        'host': 'localhost',
        'port': '5432',
    }
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY='qsfqd32ksd8qsfkaz'