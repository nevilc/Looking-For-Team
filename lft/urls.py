from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

from project.models import Project, Userdata
from project.views import UserRegisterWizard
from project.forms import UserForm, UserdataForm, UserdataInterestsForm

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lft.views.home', name='home'),
    # url(r'^lft/', include('lft.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	url(r'^$', 'project.views.home'),
	url(r'^user/login/$', 'project.views.user_login'),
	url(r'^user/logout/$', 'project.views.user_logout'),
	
	url(r'^project/create/$', 'project.views.project_create'),
	url(r'^project/(?P<project_id>\d+)/delete/$', 'project.views.project_delete'),
	
	url(r'^project/(?P<project_id>\d+)/position/create/$', 'project.views.project_createposition'),
	url(r'^project/(?P<project_id>\d+)/position/(?P<position_id>\d+)/delete/$', 'project.views.project_deleteposition'),
	url(r'^project/(?P<project_id>\d+)/position/(?P<position_id>\d+)/free/$', 'project.views.project_freeposition'),
	url(r'^project/(?P<project_id>\d+)/position/(?P<position_id>\d+)/accept/$', 'project.views.project_acceptposition'),
	url(r'^project/(?P<project_id>\d+)/position/(?P<position_id>\d+)/promote/$', 'project.views.project_promoteposition'),
	url(r'^project/(?P<project_id>\d+)/position/(?P<position_id>\d+)/demote/$', 'project.views.project_demoteposition'),
	
	url(r'^skill/reload/$', 'project.views.skill_reload'),
	url(r'^interest/reload/$', 'project.views.interest_reload'),
	
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	
	
	# /project/*
	#url(r'^project/$', 'project.views.index'),
	#url(r'^project/(?P<project_id>\d+)/$', 'project.views.detail'),
	
	
	# /user/*
	#url(r'^user/register$', 'project.views.userregister'),
	
	#url(r'^project/(?P<pk>\d+)/$',
    #    DetailView.as_view(
    #        model=Project,
    #        template_name='project/detail.html')),
	
	url(r'^project/(?P<project_id>\d+)/$', 'project.views.project_detail'),
	
	url(r'^user/(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Userdata,
            template_name='userdata/detail.html')),
			
	
	(r'^user/register/$',
		UserRegisterWizard.as_view([UserForm, UserdataForm, UserdataInterestsForm])),
)

"""
	url(r'^user/register/$',
		'project.views.user_register'),
	url(r'^user/register/2/$',
		'project.views.user_userdata'),
	url(r'^user/register/3/$',
		'project.views.user_interests'),
	url(r'^user/register/4/$',
		'project.views.user_skills'),
	"""