import logging
import time
import pic_api
import os

APP_ROOT = os.path.abspath(pic_api.__path__[0])

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s (%(lineno)s) - %(levelname)s: %(message)s",
    datefmt='%d.%m.%Y. %H:%M:%S', 
    filename=APP_ROOT + '/logs/api_engine.log'
    )

logger = logging.getLogger(__name__)

from django.core.files.storage import FileSystemStorage
from .tasks import get_resize_image_name
from celery import current_app
from celery.result import AsyncResult

import uuid



EXTENSION_DICTONARY = {
                        'image/jpeg': ['.jpeg', '.jpg'],
                        'image/png': ['.png'],
                    }

TASK_ID_COUNT = 36
MAX_VALUE = 9999
MIN_VALUE = 1


def POST_json_answer(request):
    
    arguments = get_arguments(request)

    if is_correct_arguments(arguments):
        filename = get_image_name(arguments['image'])
        save_image(filename, arguments['image'])
        task = get_resize_image_name.delay(filename, arguments['width'], arguments['height'])
        
        return {'status': 200, 'is_correct_arguments': True, 'task': task.id}

    return {'status': 400, 'is_correct_arguments': False, 'task': None}


def GET_json_answer(request):

    task_id = get_task_id(request)

    if is_correct_task_id(task_id):
        task = current_app.AsyncResult(task_id)
        if task.status == 'SUCCESS':
    
            filename = task.get()

            return {'status': '200', 'resize_pic_url': get_resize_image_url(filename)}
        else:
            logger.error("CeleryError: {}".format(task.status))
            
            return {'status': '500', 'resize_pic_url': None}
    
    return {'status': '400', 'resize_pic_url': None}


def get_task_id(request):
    
    return request.GET.get('uid')


def get_resize_image_url(filename):

    fs = FileSystemStorage()
    resize_pic_url = '/api' + fs.url(filename)
    return resize_pic_url


def is_correct_task_id(task_id):

    if task_id:
        return len(task_id) == TASK_ID_COUNT
    
    logger.error("IDError: count task_id must be = {})".format(TASK_ID_COUNT))

    return False


def save_image(filename, image):

    fs = FileSystemStorage()
    fs.save(filename, image)


def get_image_name(image):

    name = uuid.uuid4().hex
    extension = get_extension_filename(image.name)

    return name + extension


def is_correct_arguments(arguments):
 
    return value_in_range(arguments['width']) and value_in_range(arguments['height']) and is_correct_extension(arguments['image'])
    

def is_correct_extension(image):


    if image:
        
        extension_content = EXTENSION_DICTONARY.get(image.content_type)
        extension_image = get_extension_filename(image.name)

        if not extension_content:
            logger.error("ContentError: content_type must be filled")
            return False

        elif not extension_image:
            logger.error("ContentError: image extension not found")
            return False

        return extension_image in extension_content
     
    logger.error("fileError: file not found")

    return False


def get_extension_filename(name):
    value = name.split('.')
    if value:
        return '.'+value[-1]
    
    return None



def value_in_range(value):
    
    if value:
        return MIN_VALUE <= value <= MAX_VALUE
    logger.error("ValueError: value must be in range({}-{})".format(MIN_VALUE, MAX_VALUE))
    return False


def get_arguments(request):

    return {
            'width': get_width(request),
            'height': get_height(request),
            'image': get_image(request),
            }


def get_width(request):
    width = request.POST.get('width')
    try:
        width = int(width)
        return width
    except:
        logger.error("TypeError: argument 'width' must be int")
        return None


def get_height(request):
    height = request.POST.get('height')
    try:
        height = int(height)
        return height
    except:
        logger.error("TypeError: argument 'height' must be int")
        return None


def get_image(request):
    return request.FILES.get('image')