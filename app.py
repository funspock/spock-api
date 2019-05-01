import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request

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

'''
@app.route('/')
def index():
    with conn.cursor() as cursor:
        sql = 'select * from user'
        cursor.execute(sql)
        
        results = cursor.fetchall()
        return jsonify(results)
'''

@app.route("/api/login", methods = ['POST'])
def login():

    username = request.json['username']
    password = request.json['password']
     
    with conn.cursor() as cursor:
        sql = 'select * from user where username = %s'
        cursor.execute(sql, username)

        result = cursor.fetchall()
        if len(result) == 0:
            return make_response('login failed', 400)
        if result[0]['password'] == password :
            return jsonify(result)
        else :
            return make_response('login failed', 400)






if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)