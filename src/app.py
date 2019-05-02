import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request

import pymysql.cursors


app = Flask(__name__)

dotenv_path = '/projects/.env'
load_dotenv(dotenv_path)

host = os.environ.get("HST")
usr = os.environ.get("USR")
passwd = os.environ.get("PASSWD")
db = os.environ.get("DB")

print(host)

conn = pymysql.connect(host = host,
                        user = usr,
                        db = db,
                        password = passwd,
                        cursorclass = pymysql.cursors.DictCursor
)


@app.route("/")
def index():
    return 'you requested flask api server'

@app.route("/api/login", methods = ['POST'])
def login():

    username = request.json['username']
    password = request.json['password']
     
    with conn.cursor() as cursor:
        sql = 'select * from user_data where username = %s'
        cursor.execute(sql, username)

        result = cursor.fetchall()
        if len(result) == 0:
            return make_response('login failed', 400)
        if result[0]['password'] == password :
            
            with conn.cursor() as c:
                sql = 'select * from spot where user = %s'
                c.execute(sql, username)
                spot_res = c.fetchall()
                return jsonify(spot_res)

        else :
            return make_response('login failed', 400)

'''
@app.route("/api/spot", methods = ['POST'])
def post_spot():
     
     name = request.json[]
'''



if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)