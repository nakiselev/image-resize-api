from celery.result import AsyncResult
from celery import current_app
from rest_framework.response import Response
from rest_framework.views import APIView

import pic_api.api_engine as api_engine 

# Create your views here.

class PicView(APIView):
    def get(self, request):

        json_answer = api_engine.GET_json_answer(request)

        return Response(json_answer, status=json_answer['status'])
        

    def post(self, request):
        
        json_answer = api_engine.POST_json_answer(request)

        return Response(json_answer, status=json_answer['status'])