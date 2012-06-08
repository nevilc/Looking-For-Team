from django.http import HttpResponse

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext

from project.forms import UserForm
from project.models import Project

def index(request):
	recent_project_list = Project.objects.all().order_by('-update_date')[:5]
	return render_to_response('project/index.html', {'recent_project_list', recent_project_list})
	
def detail(request, project_id):
	p = get_object_or_404(Project, pk=project_id)
	return render_to_response('project/detail.html', {'project': p})

class user:
	@staticmethod
	def register(request):
		form = UserForm(request.POST or None)
		if form.is_valid():
			newuser = form.save()
			#newuser.save()
			return redirect(user.userdata, user=newuser)
		
		return render_to_response('user/register.html', {}, context_instance=RequestContext(request));

	def userdata(request, user):
		form = UserdataForm(request.POST or None)
		if form.is_valid():
			user.save()
			newuserdata = form.save()
			newuserdata.user = user
			newuserdata.save()
			return redirect('user/interests.html', 