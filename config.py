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
    SECRET_KEY='kkkWgAXfHAIPLqVSHSu7i2Pn5cWYrVTinXWcsiRs-5o'
    JWT_SECRET_KEY='kkkWgAXfHAIPLqVSHSu7i2Pn5cWYrVTinXWcsiRs-5o'
