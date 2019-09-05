from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^events$', views.events),
    url(r'^create$', views.create),
    url(r'^add_event$', views.add_event),
    url(r'^events$', views.events),
    url(r'^view_event/(?P<id>\d+)$', views.view_event),
    url(r'^cancel_event/(?P<id>\d+)$', views.cancel_event),
    url(r'^join_event/(?P<id>\d+)$', views.join_event),



]

