
## description

simple api for resizing image


## installing


1. git clone https://github.com/nakiselev/image-resize-api.git

2. create virtual environment 
```bash
python3 -m venv myvenv 
```
3. activate venw  
```bash
source myvenv/bin/activate
```

next steps use in path with manage.py!!!

4. install requirements
```bash
pip install -r requirements.txt
```
5. install redis 
```bash
brew install redis
```

## running

1.  migrate db
```bash
python3 manage.py migrate
```

2. in new terminal
```bash
redis-server
```
3. in new terminal activate venv   and use 
```bash
celery -A simple_api_pic worker -l info
```

4. start server
```bash
python3 manage.py runserver
```

## stop

django

control-c

redis 
```bash
redis-cli shutdown
```

celery
```bash
pkill -9 -f 'celery worker'
```

## test

```bash
python3 manage.py test
```

api link

http://127.0.0.1:8000/api/pic/

POST:
params {
		image: file - image(jpg,png),
		width: number in range 1-9999,
		height: number in range 1-9999
}

response {
		status: HTTP status,
		'is_correct_arguments': True/False,
		task: task_id/none
}


GET:
	params {
			uid: task_id 
}

response {
		status: HTTP status,
		resize_pic_url: url/none
}







