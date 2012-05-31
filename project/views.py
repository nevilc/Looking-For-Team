from django.http import HttpResponse

from django.shortcuts import render_to_response, get_object_or_404

from project.models import Project

def index(request):
	recent_project_list = Project.objects.all().order_by('-update_date')[:5]
	return render_to_response('project/index.html', {'recent_project_list', recent_project_list})
	
def detail(request, project_id):
	p = get_object_or_404(Project, pk=project_id)
	return render_to_response('project/detail.html', {'project': p})
	
