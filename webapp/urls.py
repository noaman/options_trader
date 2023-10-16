from django.conf.urls import include
from django.urls import path

from django.urls import re_path
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.showDashboard, name='Index'),
    re_path(r'^heatmap/$', views.showHeatmap,name='trends'),
    re_path(r'^heatmap/(?P<sort>.*)/$', views.showHeatmap,name='trends'),
    re_path(r'^screeners/$', views.showScreener,name='trends'),
    re_path(r'^screeners/(?P<scrip>.*)/$', views.showScreener,name='trends'),
    re_path(r'^top20/$', views.showTop20,name='trends'),
    re_path(r'^df/$', views.showDataframe,name='trends'),
    re_path(r'^gen20DFuturesBU.*$', views.gen20DFuturesBU , name = 'gen20DFuturesBU'),
    path('refresh_json/' , views.refresh_json, name = 'refresh_json'),
    path('futuresOptionsMR/', views.getFuturesOptionsMR, name = 'FuturesOptionsMR'),
    path('20DFuturesBU/', views.load20DFuturesBU, name = '20DFuturesBU')
    #path('gen20DFuturesBU/', views.gen20DFuturesBU , name = 'gen20DFuturesBU')
    
    # url(r'^trends/$', views.showTrends,name='trends'),


    # url(r'^charts/(?P<symbol>.*)/$', views.showCharts,name='charts'),
    # url(r'^charts/$', views.showCharts,name='charts'),
]