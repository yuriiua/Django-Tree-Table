
from django.conf.urls import url, include
from emTrTable.views import *
from . import views as core_views
from django.contrib.auth import login
from rest_framework.decorators import action
from rest_framework import routers, views
from emTrTable.views import EmployeeViewSet



router = routers.DefaultRouter()
router.register(r'EmployeeViewSet', EmployeeViewSet, basename='EmployeeView')

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^$', index),
    url(r'^jsonTableAll', getjsonTable),
    url(r'^jsonTableByID', getTableByBossId),
    url(r'^searchBy', serchby),
    url(r'^detailPage', detailPage),
    url(r'^api/', include(router.urls)),
]
