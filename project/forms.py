from django.db import models
from django.core import validators
from django import forms

from widgets import RankingWidget

from django.forms import ModelForm, Form

from project.models import Userdata, Project, Position, Interest, Skill, UserInterest, UserSkill
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.models import fields_for_model, ModelMultipleChoiceField
from django.forms import ValidationError


class UserForm(Form):
	username = fields_for_model(User, ['username'])['username']
	password = fields_for_model(User, ['password'])['password']
	password_confirm = fields_for_model(User, ['password'])['password']
	password_confirm.label = "Confirm password"
	
	email = fields_for_model(User, ['email'])['email']
	email.required = True
	email_confirm = fields_for_model(User, ['email'])['email']
	email_confirm.label = "Confirm E-mail"
	email_confirm.required = True
	
	first_name = fields_for_model(User, ['first_name'])['first_name']
	last_name = fields_for_model(User, ['last_name'])['last_name']
	
	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		
		user_password = cleaned_data.get("password")
		user_password_confirm = cleaned_data.get("password_confirm")
		
		if user_password != user_password_confirm:
			raise ValidationError("Entered passwords do not match")
			
		user_email = cleaned_data.get("email")
		user_email_confirm = cleaned_data.get("email_confirm")
		
		if user_email != user_email_confirm:
			raise ValidationError("Entered emails do not match")
		
		return cleaned_data
	
class UserdataForm(Form):
	avatar = fields_for_model(Userdata, ['avatar'])['avatar']
	bio = fields_for_model(Userdata, ['bio'])['bio']
	url = fields_for_model(Userdata, ['url'])['url']
	
class UserdataInterestsForm(Form):
	#interests = fields_for_model(Userdata, ['interests'])['interests']
	interests = ModelMultipleChoiceField(queryset=Interest.objects.filter(active=True))

class UserdataSkillsForm(Form):
	#test = forms.IntegerField(required=False)

	def __init__(self, *args, **kwargs):
		#extra_fields = kwargs.pop('extra', 0)
		super(UserdataSkillsForm, self).__init__(*args, **kwargs)
		
		self.fields['workaround'] = forms.IntegerField(required=False)
		
		for skill in Skill.objects.filter(active=True):
			#if skill.active:
			self.fields[str(skill.id)] = forms.IntegerField(
				label=skill.title, 
				validators=[validators.MinValueValidator(Skill.value_range[0]), validators.MaxValueValidator(Skill.value_range[1])],
				widget=RankingWidget,
				required=False)
					
	
"""
class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = (
			'title',
			'description',
			'open',
			'url',
			'interests',
		)
	
	def clean(self):
		cleaned_data = super(ContactForm, self).clean()
		
"""

class ProjectForm(Form):
	title = fields_for_model(Project, ['title'])['title']
	description = fields_for_model(Project, ['description'])['description']
	open = fields_for_model(Project, ['open'])['open']
	url = fields_for_model(Project, ['url'])['url']
	
	interests = ModelMultipleChoiceField(queryset=Interest.objects.filter(active=True), required=False)

"""	
class PositionForm(Form):
	#project = forms.ModelChoiceField(Project, editable=False)

	title = fields_for_model(Position, ['title'])['title']
	description = fields_for_model(Position, ['description'])['description']
"""
	
#"""
class PositionForm(ModelForm):
	class Meta:
		model = Position
		fields = (
			'title',
			'description',
			
		)
#"""
	
#class Userdata
	
#class RankingForm(Form):
#	skill = fields_for_model(Ranking, ['skill'])
#	rank = fields_for_model(Ranking, ['rank'])
	
class LoginForm(Form):
	username = fields_for_model(User, ['username'])['username']
	password = fields_for_model(User, ['password'])['password']
	
	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		
		self.user_cache = authenticate(username=cleaned_data.get("username"), password=cleaned_data.get("password"))
		
		if self.user_cache is None:
			raise ValidationError("User and password combination not found")
		
		return cleaned_data
		
	