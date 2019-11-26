import os
from dotenv import load_dotenv
load_dotenv()




class Config(object):
  DEBUG=True
  SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
  SECRET_KEY='supersecret'
  FLASK_ADMIN_SWATCH = 'cerulean'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  API_KEY=os.environ.get('API_KEY')
