from django.conf.urls import url, include
from .views import mine

urlpatterns = [
    url(r'^mine/$', mine, name='mine'),
]