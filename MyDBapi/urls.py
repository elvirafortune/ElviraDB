from django.conf.urls import patterns, url
from MyDBapp import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url( r'^(?P<entity>\S+)/(?P<function>\S+)$', views.choose_entity)
)

