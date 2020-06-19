from django.urls import path
from .views import PicView
from django.conf.urls.static import static
from django.conf import settings


app_name = 'pic_api'

urlpatterns = [
    path('pic/', PicView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)