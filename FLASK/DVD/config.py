# Basic Configuration
SECRET_KEY = 'add_super-secret-key-here'

SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': 'dvd',
    'host': 'localhost',
    'port': '5432',
}
SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
