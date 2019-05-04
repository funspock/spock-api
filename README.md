##接続確認
	host:port/ [method = 'GET']
	
接続できていたらyou requested flask api serverってでる。

	
##ユーザ認証
	host:port/api/login [method = 'POST']

	{
		'username':'ほげほげ', 
		'password':'ほげほげ'
	} 
	Content-Type : application/json

一致するユーザが存在したら、そのユーザの保存したデータが返ってくる。
認証に失敗した場合、400が返ってくる。


##データのポスト
	host:port/api/post [method = 'POST'] 

	{
		'img' : jpegファイル,

		'usernname' : 存在するユーザ, 
 
		'memo' : 'メモ（NULL可)', 
 
		'spot_name' : '場所の名前(Null不可)',
 
	}
	Content-Type : multipart/form-data
	
処理に成功した場合、データベースに保存されたデータが返ってくる。
	

##ユーザの作成
	host:port/api/create_user [method = 'POST']
	{
		'username' : 'ほげほげ',
		'password' : 'ほげほげ',
	}
	Content-Type : application/json
	
被っているユーザ名が存在する場合400が返ってくる。
登録に成功した場合、200が返ってくる。
 



