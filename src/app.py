import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request
import boto3

import pymysql.cursors


app = Flask(__name__)

dotenv_path = '/projects/.env'
load_dotenv(dotenv_path)

host = os.environ.get("HST")
usr = os.environ.get("USR")
passwd = os.environ.get("PASSWD")
db = os.environ.get("DB")
access_key = os.environ.get("AWS_ACCESS_KEY")
secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
bucket_name = os.environ.get("BUCKET_NAME")

s3 = boto3.client('s3',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_key,
)

s3.list_buckets()


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


@app.route("/api/post", methods = ['POST'])
def post_spot():
    
    img = request.files['img']
    username = request.form['username']
    
    try:
        s3.upload_fileobj(
            img,
            bucket_name,
            username + '/' + img.filename,
            ExtraArgs = {
                "ACL": "public-read",
                "ContentType" : img.content_type
            }
        )

        return 'https://s3.amazonaws.com/' + bucket_name + '/' + username + '/' + img.filename
    
    except Exception as e:
        print('error', e)
        return e





if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True)