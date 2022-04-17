import os
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse
from pathlib import Path

from pyramid.renderers import render_to_response

from datetime import datetime
from time import time

import mysql.connector as mysql
from dotenv import load_dotenv

base_path = str(Path(__file__).parent)

# Credentials
load_dotenv(base_path + '/credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

# SQL
db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
cursor = db.cursor()

def index_page(req):
  return FileResponse(base_path + '/index.html')

def retrieve_data(req):
    # fill query here
    meterID = str(req.matchdict['meter_id'])
    query = "SELECT * FROM Meters WHERE ID = %s;"
    cursor.execute(query, [meterID])
    try:
        record, = cursor.fetchone()
    except TypeError:
        return {'available': False}

    return 0


if __name__ == '__main__':
    with Configurator() as config:

        # config.include('pyramid_jinja2')
        # config.add_jinja2_renderer('.html')

        config.add_route('home', '/')
        config.add_view(index_page, route_name='home')

        config.add_route('data', '/data/{meter_id}')
        config.add_view(retrieve_data, route_name='data', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
    
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 6543, app)
    print('Web server started on: http://0.0.0.0:6543')
    server.serve_forever()
    db.close()
    