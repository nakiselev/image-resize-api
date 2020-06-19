
## description

simple api for resizing image


## installing


1. git clone https://github.com/nakiselev/image-resize-api.git

2. create virtual environment python3 -m venv myvenv 

3. activate venw  source myvenv/bin/activate

4. pip install -r requirements.txt

5. install redis brew install redis


## running

1. python3 manage.py migrate


in new terminal

redis-server

in new terminal

activate venv   celery worker -A simple_api_pic -l debug


2. python3 manage.py runserver
