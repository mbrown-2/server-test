import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv

from pathlib import Path

base_path = str(Path(__file__).parent)

# Credentials
load_dotenv(base_path + '/credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()

# Below is an abstract table, NOT FINAL
# Can split into different tables (whatever we want as time goes on)

cursor.execute("DROP TABLE IF EXISTS Meters;")

try:
    cursor.execute("""
    CREATE TABLE Meters (
        id           integer AUTO_INCREMENT PRIMARY KEY,
        meterName    VARCHAR(50) NOT NULL,
        wifi         VARCHAR(50) NOT NULL,
        moisture     VARCHAR(50) NOT NULL,
        sunlight     VARCHAR(50) NOT NULL,
        temperature  VARCHAR(50) NOT NULL,
        remRate      INT(10) NOT NULL,
        dimXY        INT(10) NOT NULL,
        breed        VARCHAR(50) NOT NULL
    );
    """)

    cursor.execute('describe Meters')
    print(cursor.fetchall())
except RuntimeError as err:
    print("runtime error: {0}".format(err))

cursor.close()
db.commit()