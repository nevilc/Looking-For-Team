from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lft.views.home', name='home'),
    # url(r'^lft/', include('lft.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	
	
	# /project/*
	url(r'^project/$', 'project.views.index'),
	url(r'^project/(?P<project_id>\d+)/$', 'project.views.detail'),
)
