from project.models import Project, Position, Skill, Userdata

from django.contrib import admin

admin.site.register(Userdata)

admin.site.register(Project)
admin.site.register(Position)

#admin.site.register(Skill)