from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('show/<report_name>/', report, name='show'),
    path('index_admin', index_admin, name='index_admin'),
    path('user', users, name='user'),
    path('home/', index, name='report'),
    path('update_report', update_report, name='update_report'),
   # path('supervisor_index', supervisor_index, name='supervisor_index'),
    re_path(r'^.*\.*', pages, name='pages'),
]

