import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, jsonify
import pymysql.cursors


app = Flask(__name__)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

host = os.environ.get("HOST")
usr = os.environ.get("USR")
passwd = os.environ.get("PASSWD")
db = os.environ.get("DB")


conn = pymysql.connect(host = host,
                        user = usr,
                        db = db,
                        password = passwd,
                        cursorclass = pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    with conn.cursor() as cursor:
        sql = 'select * from user'
        cursor.execute(sql)
        
        results = cursor.fetchall()
        return jsonify(results)




if __name__ == '__main__':
    app.run(host = '0.0.0.0')