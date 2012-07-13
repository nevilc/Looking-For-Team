from django.http import HttpResponse

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.formtools.wizard.views import SessionWizardView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

import datetime
import yaml

from project.forms import UserForm, LoginForm, ProjectForm, PositionForm
from project.models import Project, User, Userdata, Position, Interest, Skill, ProjectRelation, admin_position_default

# not views, just helper functions!
def can_edit_project(request, project):
	if request.user:
		#is logged in
		try:
			p_rel = ProjectRelation.objects.get(user=request.user.userdata, project=project)
			# is member
			if p_rel.admin:
				# is admin
				return True
		except ObjectDoesNotExist:
			pass
	return False
	
def require_project_admin(request, project):
	if not can_edit_project(request, project):
		return HttpResponse('Unauthorized', status=401)
		
def project_has_position(project, position):
	return position.project == project

def require_project_position_match(project, position):
	# ensure position actually belongs to project
	if not project_has_position(project, position):
		# if this happens, it's probably someone mucking with ill-intent, so 401
		return HttpResponse('Unauthorized', status=401)
		
def project_has_member(project, user):
	# check if user is already in the project
	try:
		ProjectRelation.objects.get(user=user, project=project)
	except ObjectDoesNotExist:
		return False
	return True
		
def require_project_member(request, project):
	if not project_has_member(project, request.user.userdata):
		# not really a proper response, but will do for now
		return HttpResponse('Unauthorized', status=401)
		
def require_project_nonmember(request, project):
	if project_has_member(project, request.user.userdata):
		# not really a proper response, but will do for now
		return HttpResponse('Unauthorized', status=401)
		
# End helper functions


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
	
	return render_to_response('project/detail.html', {'project': p, 'can_edit': can_edit_project(request, p), 'is_member': project_has_member(p, request.user.userdata)}, context_instance=RequestContext(request))
	
@login_required
def project_create(request):
	#template_project = Project()

	#form = ProjectForm(request.POST or template_project)
	form = ProjectForm(request.POST or None, initial={})
	if form.is_valid():
		new_project = form.save()
		
		new_position = admin_position_default
		
		new_position.project = new_project
		
		#new_position.save()
		
		relation = ProjectRelation(admin=True, user=request.user.userdata, project=new_project)
		relation.save()
		
		new_position.project_relation = relation
		new_position.save()
		
		
		admin_position_default.id=None
		
		
		return redirect(project_detail, new_project.id)
	
	return render_to_response('project/create.html', {'form': form}, context_instance=RequestContext(request))

@login_required
def project_delete(request, project_id):
	p = get_object_or_404(Project, pk=project_id)
	
	require_project_admin(request, p)
	
	# cascading should take care of everything
	
	p.delete()
	
	return redirect(home)
	
@login_required
def project_createposition(request, project_id):
	p = get_object_or_404(Project, pk=project_id)
	
	require_project_admin(request, p)
	
	pos = Position(project=p)
	
	form = PositionForm(request.POST or None, instance=pos)
	
	if form.is_valid():
		pos = form.save()
		
		return redirect(project_detail, p.id)
		
	return render_to_response('project/newposition.html', {'form': form}, context_instance=RequestContext(request))
	
@login_required
def project_deleteposition(request, project_id, position_id):
	p = get_object_or_404(Project, pk=project_id)
	pos = get_object_or_404(Position, pk=position_id)
	
	require_project_admin(request, p)
	
	require_project_position_match(p, pos)
	
	pr = ProjectRelation.objects.get(user=request.user.userdata, project=p)
	
	#pr.delete()
	pos.delete()
	
	return redirect(project_detail, p.id)
	
@login_required
def project_freeposition(request, project_id, position_id):
	# 'fire' whoever holds the given position
	p = get_object_or_404(Project, pk=project_id)
	pos = get_object_or_404(Position, pk=position_id)
	
	require_project_admin(request, p)
	
	require_project_position_match(p, pos)
	
	if not pos.project_relation:
		# position exists, but not filled, so no one to 'fire'
		# not sure what the actual response should be
		return HttpResponse('Position is not filled', status=404)
	
	pr = ProjectRelation.objects.get(user=pos.project_relation.user, project=p)
		
	pr.delete()
	
	return redirect(project_detail, p.id)
	
	
@login_required
def project_acceptposition(request, project_id, position_id):
	p = get_object_or_404(Project, pk=project_id)
	pos = get_object_or_404(Position, pk=position_id)
	
	# for now, users will just add themselves
	#require_project_admin(request, p)
	
	require_project_position_match(p, pos)
	
	require_project_nonmember(request, p)
	
	rel = ProjectRelation(
		user = request.user.userdata,
		project = p,
		admin = False,
	)
	
	rel.save()
	
	pos.project_relation = rel
	
	pos.save()
	
	return redirect(project_detail, p.id)
	
@login_required
def project_promoteposition(request, project_id, position_id):
	p = get_object_or_404(Project, pk=project_id)
	pos = get_object_or_404(Position, pk=position_id)
	
	require_project_admin(request, p)
	
	require_project_position_match(p, pos)
	
	if not pos.project_relation:
		# position exists, but not filled, so no one to 'fire'
		# not sure what the actual response should be
		return HttpResponse('Position is not filled', status=404)
	
	pr = ProjectRelation.objects.get(user=pos.project_relation.user, project=p)
	
	pr.admin = True
	
	pr.save()
	
	return redirect(project_detail, p.id)
	
@login_required
def project_demoteposition(request, project_id, position_id):
	p = get_object_or_404(Project, pk=project_id)
	pos = get_object_or_404(Position, pk=position_id)
	
	require_project_admin(request, p)
	
	require_project_position_match(p, pos)
	
	if not pos.project_relation:
		# position exists, but not filled, so no one to 'fire'
		# not sure what the actual response should be
		return HttpResponse('Position is not filled', status=404)
	
	pr = ProjectRelation.objects.get(user=pos.project_relation.user, project=p)
	
	pr.admin = False
	
	pr.save()
	
	return redirect(project_detail, p.id)

@staff_member_required
def interest_reload(request):
	start_time = datetime.datetime.now()

	interest_stream = file('data/interests.yaml', 'r')
	interest_yaml_file = yaml.load(interest_stream)
	
	def process_interest(parent_interest, interest_yaml):
		if not 'name' in interest_yaml:
			print "Missing name in interest"
			return redirect(home)
		name = interest_yaml['name']
		if 'description' in interest_yaml:
			description = interest_yaml['description']
		else:
			description = default_description
		
		interest = Interest.objects.get_or_create(title=name)[0]
		
		interest.active = True
		interest.description = description
		interest.parent = parent_interest
		
		interest.save()
		
		if 'subs' in interest_yaml:
			for child in interest_yaml['subs']:
				process_interest(interest, child)
		
	default_description = ""
		
	if 'default_description' in interest_yaml_file:
		default_description = interest_yaml_file['default_description']
	
	if 'interests' in interest_yaml_file:
		interest_yaml_root = interest_yaml_file['interests']
		for interest_yaml in interest_yaml_root:
			process_interest(None, interest_yaml)
	else:
		print "Invalid interest datafile"
		return redirect(home)
	
	# deactivate all interests that are no longer in the YAML
	# prevents typoes from wreaking havoc
	Interest.objects.filter(update_date__lt=start_time).update(active=False)
	
	return redirect(home)
	
@staff_member_required
def skill_reload(request):
	start_time = datetime.datetime.now()

	skill_stream = file('data/skills.yaml', 'r')
	skill_yaml_file = yaml.load(skill_stream)
	
	def process_skill(parent_skill, skill_yaml):
		if not 'name' in skill_yaml:
			print "Missing name in skill"
			return redirect(home)
		name = skill_yaml['name']
		if 'description' in skill_yaml:
			description = skill_yaml['description']
		else:
			description = default_description
		if 'levels' in skill_yaml:
			levels = skill_yaml['levels']
		else:
			levels = default_levels
		
		#try:
		#	skill = Skill.objects.get(title=name)
		#except ObjectDoesNotExist:
		#	skill = Skill(title=name)
		
		skill = Skill.objects.get_or_create(title=name)[0]
		
		skill.active = True
		skill.description = description
		#skill.levels
		skill.parent = parent_skill
		
		skill.save()
		
		if 'subs' in skill_yaml:
			for child in skill_yaml['subs']:
				process_skill(skill, child)
		
		
		
		
	default_levels = []
	default_description = ""
	
	if 'default_levels' in skill_yaml_file:
		default_levels = skill_yaml_file['default_levels']
		
	if 'default_description' in skill_yaml_file:
		default_description = skill_yaml_file['default_description']
	
	if 'skills' in skill_yaml_file:
		skill_yaml_root = skill_yaml_file['skills']
		for skill_yaml in skill_yaml_root:
			process_skill(None, skill_yaml)
	else:
		print "Invalid skill datafile"
		return redirect(home)
	
	# deactivate all skills that are no longer in the YAML
	# prevents typoes from wreaking havoc
	Skill.objects.filter(update_date__lt=start_time).update(active=False)
	
	return redirect(home)
	
	
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


