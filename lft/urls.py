from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from project.models import Project, Userdata

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
	#url(r'^project/$', 'project.views.index'),
	#url(r'^project/(?P<project_id>\d+)/$', 'project.views.detail'),
	
	
	# /user/*
	#url(r'^user/register$', 'project.views.userregister'),
	
	url(r'^project/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Project,
            template_name='project/detail.html')),
	
	url(r'^user/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Userdata,
            template_name='userdata/detail.html')),
			
	url(r'^user/new/$',
		'project.views.usernew'),
)
