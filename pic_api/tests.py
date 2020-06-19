from django.test import TestCase
from django.test.client import Client
import os
import pic_api
import  random


APP_ROOT = os.path.abspath(pic_api.__path__[0])
SUCCESS = 200
INCORRECT_HEADER = 400

NUMBER_OF_TRY = 10

ARGS = [
        {'width': 50, 'height': 50, 'image': open(APP_ROOT+'/664a506ef99e4f1ebcdb4bc94883ec99.jpeg','rb')},
        {'width': 100, 'height': 100, 'image': open(APP_ROOT+'/664a506ef99e4f1ebcdb4bc94883ec99.jpeg','rb')}
       ]



class apiTest(TestCase):

    def __init__(self, *a, **kw):
        super(apiTest, self).__init__(*a, **kw)
        self.host = '127.0.0.1:8000'
        self.command = 'api/pic/'
        self.url = 'http://{}/{}'.format(self.host, self.command)
        self.client = Client()

    def test_post(self):
        arg = random.choice(ARGS)
        status_code, text = self._post_response(arg)

        self.assertEqual(status_code, SUCCESS)

    def test_get(self):

        arg = random.choice(ARGS)
        status_code, text = self._post_response(arg)
        uid_id = text['task']

        for t in range(NUMBER_OF_TRY):
            status_code, text = self._get_response(uid_id)
        
        self.assertEqual(status_code, SUCCESS)


    def _get_response(self, uid):
        values = {'uid': uid}
        _response = self.client.get(self.url, values)
        return _response.status_code, _response.json()

    def _post_response(self, values):
        _response = self.client.post(self.url, values)
        return _response.status_code, _response.json()
