from django.conf.urls import patterns, url
from MyDBapp import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url( r'^db/api/(?P<entity>\S+)/(?P<function>\S+)$', views.choose_entity),
    url( r'^db/api/clear$', views.deleteAll)
)

