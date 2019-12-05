import os
from dotenv import load_dotenv
load_dotenv()




class Config(object):
  SECRET_KEY = os.environ.get("FLASK_SECRET_KEY") or "supersekrit"
  SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_POSTGRES') or os.environ.get('DATABASE_URL')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  FACEBOOK_OAUTH_CLIENT_ID = os.environ.get("FACEBOOK_OAUTH_CLIENT_ID")
  FACEBOOK_OAUTH_CLIENT_SECRET = os.environ.get("FACEBOOK_OAUTH_CLIENT_SECRET")
  FLASK_ADMIN_SWATCH = 'cerulean'
  API_KEY=os.environ.get('API_KEY')
  DEBUG=True
  URL=os.environ.get('URL')
