from django.http import HttpResponse

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required

from django.conf import settings

from project.forms import UserForm, LoginForm, ProjectForm
from project.models import Project, User, Userdata, Position, ProjectRelation, admin_position_default

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

def project_detail(request, project_id):
	p = get_object_or_404(Project, pk=project_id)
	return render_to_response('project/detail.html', {'project': p})
	
@login_required
def project_create(request):
	#template_project = Project()

	#form = ProjectForm(request.POST or template_project)
	form = ProjectForm(request.POST or None, initial={})
	if form.is_valid():
		new_project = form.save()
		
		new_position = admin_position_default
		
		new_position.project = new_project
		
		new_position.save()
		
		relation = ProjectRelation(admin=True, user=request.user.userdata, project=new_project, position=new_position)
		
		relation.save()
		
		admin_position_default.id=None
		
		
		return redirect(project_detail, new_project.id)
	
	return render_to_response('project/create.html', {'form': form}, context_instance=RequestContext(request))
		
@login_required
def project_newposition(request, project_id):
	p = get_object_or_404(Project, pk=project_id)
	
	pr = ProjectRelation.objects.get(user=request.user, project=p)
	
	if pr == None or not pr.admin:
		return HttpResponse('Unauthorized', status=401)
	
	form = PositionForm(request.POST or None)
	
	if form.is_valid():
		pos = form.save()
		
		

	
	
	
	
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


