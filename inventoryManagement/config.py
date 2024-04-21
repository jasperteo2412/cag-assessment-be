from app import app
from dotenv import load_dotenv
from flaskext.mysql import MySQL
import os

load_dotenv()

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv('DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('DATABASE')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('DATABASE_URL')

mysql.init_app(app)