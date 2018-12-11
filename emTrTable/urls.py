
from django.conf.urls import url
from emTrTable import views
from . import views as core_views
from django.contrib.auth import login

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^$', views.index),
    url(r'^jsonTableAll', views.getjsonTable),
    url(r'^jsonTableByID', views.getTableByBossId),
    url(r'^searchBy', views.serchby),
    url(r'^detailPage', views.detailPage)
]
