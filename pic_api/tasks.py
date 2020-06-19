from django.core.files.storage import FileSystemStorage
from celery import shared_task
from PIL import Image, ImageFile
import logging
import os
import pic_api

APP_ROOT = os.path.abspath(pic_api.__path__[0])

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s (%(lineno)s) - %(levelname)s: %(message)s",
    datefmt='%d.%m.%Y. %H:%M:%S', 
    filename=APP_ROOT + '/logs/celery.log'
    )

logger = logging.getLogger(__name__)


@shared_task
def get_resize_image_name(name, width, height):


    ImageFile.LOAD_TRUNCATED_IMAGES = True
    fs = FileSystemStorage()

    path = '{}/{}'.format(fs.base_location, name)

    with Image.open(path) as img:
        try:
            img = img.resize((width, height))
            img.save(path)
        except Exception as error:
            logger.error("{} Filename: {}".format(error, name))
        

    return name

