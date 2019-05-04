import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request
import boto3
from werkzeug import secure_filename
import pymysql.cursors

ALLOWED_EXTENSIONS = set(['jpg','jpeg'])

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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

        #No username matched
        if len(result) == 0:
            return make_response('login failed', 400)

        if result[0]['password'] == password :
            
            with conn.cursor() as c:
                sql = 'select * from spot_data where user = %s'
                c.execute(sql, username)
                spot_res = c.fetchall()
                return jsonify(spot_res)

        else :
            return make_response('login failed', 400)

@app.route("/api/create_user", methods = ['POST'])
def create_user():
    username = request.json['username']
    password = request.json['password']

    try :
        with conn.cursor() as cursor:
            sql = 'insert into user_data values(%s, %s)'
            cursor.execute(sql, (username, password))
        
        conn.commit()
        return make_response('success', 200)

    except Exception as e:
        return make_response(e, 400)

@app.route("/api/post", methods = ['POST'])
def post_spot():
    
    spot_name = request.form['spot_name']
    memo = request.form['memo']
    img = request.files['img']
    username = request.form['username']


    print(
        'spot_name', spot_name,
        'memo', memo,
        'img', img.filename,
        'username', username
    )

    if not (img.filename and allowed_file(img.filename)):
        return make_response('image file is not supported', 400)
    

    try:
        #upload posted image to S3
        s3.upload_fileobj(
            img,
            bucket_name,
            username + '/' + secure_filename(img.filename),
            ExtraArgs = {
                "ACL": "public-read",
                "ContentType" : 'image/jpeg',
            }
        )

        #image url in S3
        img_url = 'https://s3.amazonaws.com/' + bucket_name + '/' + username + '/' + img.filename


        #insert spot_data
        with conn.cursor() as c:
            sql = 'insert into spot_data (name, memo, photo_url, user) values(%s, %s, %s, %s)'
            c.execute(sql, (spot_name, memo, img_url, username))
        conn.commit()

        #get inserted spot_data
        with conn.cursor() as data:
            sql = 'select * from spot_data where id = %s'
            data.execute(sql, c.lastrowid)
            res = data.fetchall()
            return jsonify(res)
    
    except Exception as e:

        return make_response(e, 400)


@app.route('/api/delete_spot', methods = ['POST'])
def delete_spot():
    item_id = request.json['item_id']
    username = request.json['username']

    try :
        with conn.cursor() as data:
            sql = 'select * from spot_data where id = %s'
            data.execute(sql, item_id)
            res = data.fetchall()

            if len(res) == 0:
                return make_response('item is not exist on server', 400)

            if res[0]['user'] == username :
                
                with conn.cursor() as c : 
                    del_sql = 'delete from spot_data where id = %s'
                    c.execute(del_sql, item_id)
                
                conn.commit()
                return make_response('success', 200)
            
            else :
                return make_response('you did not create this data', 400)

    except Exception as e :
        return make_response(e, 400)


if __name__ == '__main__':
    app.run(host = '0.0.0.0')