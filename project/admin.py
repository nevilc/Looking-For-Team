from project.models import Project, Position, Interest, Skill, Userdata, ProjectRelation, UserInterest, UserSkill, ProjectInterest, PositionSkill

from django.contrib import admin

admin.site.register(Userdata)

admin.site.register(Project)
admin.site.register(Position)

admin.site.register(Skill)
admin.site.register(Interest)

admin.site.register(ProjectRelation)

# test
admin.site.register(UserInterest)
admin.site.register(UserSkill)

admin.site.register(ProjectInterest)
admin.site.register(PositionSkill)
