host:ip/ [method = 'GET']
接続できていたらyou requested flask api serverってでる

host:ip/api/login [method = 'POST'] {'username':'ほげほげ', 'password':'ほげほげ'}
一致するユーザが存在したら、そのユーザの保存したデータが返ってくる
認証に失敗した場合、400が返ってくる

想定外のリクエストが投げられたらつらい。

