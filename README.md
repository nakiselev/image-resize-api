
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
celery -A proj worker -l info
```

4. start server
```bash
python3 manage.py runserver
```
