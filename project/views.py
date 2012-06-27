from django.http import HttpResponse

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage

from django.conf import settings

from project.forms import UserForm, LoginForm
from project.models import Project, User, Userdata

def home(request):
	return render_to_response('index.html', {}, context_instance=RequestContext(request))
	
def user_login(request):
	form = LoginForm(request.POST or None)
	if form.is_valid():
		login(request, form.user_cache)
		return redirect(home)
	return render_to_response('user/login.html', {'form':form}, context_instance=RequestContext(request))
	
def user_logout(request):
	logout(request)
	return redirect(home)

def index(request):
	recent_project_list = Project.objects.all().order_by('-update_date')[:5]
	return render_to_response('project/index.html', {'recent_project_list', recent_project_list})
	
def detail(request, project_id):
	p = get_object_or_404(Project, pk=project_id)
	return render_to_response('project/detail.html', {'project': p})

"""
class user:
	@staticmethod
	def register(request):
		form = UserForm(request.POST or None)
		if form.is_valid():
			newuser = form.save()
			#newuser.save()
			return redirect(user.userdata, user=newuser)
		
		return render_to_response('user/register.html', {}, context_instance=RequestContext(request))

	@staticmethod
	def userdata(request, user):
		form = UserdataForm(request.POST or None)
		if form.is_valid():
			user.save()
			newuserdata = form.save()
			newuserdata.user = user
			newuserdata.save()
			login(request, user)
			return redirect(user.interests, user=user) 
		
		return render_to_response('user/userdata.html', {}, context_instance=RequestContext(request))
		
	@staticmethod
	def interests(request, user):
		form = UserdataInterestsForm(request.Post or None)
		if form.is_valid():
			#user.
			return redirect(user.skills, user=user)
			
		return render_to_response('user/interests.html', {}, context_instance=RequestContext(request))
		
	@staticmethod
	def skills(request, user):
		form = UserdataSkillsForm(request.Post or None)
		if form.is_valid():
			#
			return redirect(home, {})
"""
class UserRegisterWizard(SessionWizardView):
	template_name = 'user/register.html'
	
	file_storage = FileSystemStorage(location=settings.MEDIA_ROOT+"temp/", base_url=settings.MEDIA_URL+"temp/")

	def done(self, form_list, **kwargs):
		user = User.objects.create_user(form_list[0].cleaned_data['username'], form_list[0].cleaned_data['email'], form_list[0].cleaned_data['password'])
		user.first_name = form_list[0].cleaned_data['first_name']
		user.last_name = form_list[0].cleaned_data['last_name']
		
		user.save()
		
		auth_user = authenticate(username=user.username, password=form_list[0].cleaned_data['password'])
		
		userdata = Userdata(
					user=user, 
					avatar=form_list[1].cleaned_data['avatar'], 
					bio=form_list[1].cleaned_data['bio'],
					url=form_list[1].cleaned_data['url'])
		
		userdata.save()
		#login(, auth_user)
		
		return redirect(home)


