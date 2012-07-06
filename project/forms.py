from django.forms import ModelForm, Form

from project.models import Userdata, Ranking, Tag, Project
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.forms.models import fields_for_model
from django.forms import ValidationError

"""
class UserForm(ModelForm):
	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password',
			
		)
		#exclude = (

class UserdataForm(ModelForm):
	class Meta:
		model = Userdata
		fields = (
			'avatar',
			'bio',
			'url',
		)
		
class UserdataInterestsForm(ModelForm):
	class Meta:
		model = Userdata
		fields = {
			#'interests',
		}
		
class UserdataSkillsForm(ModelForm):
	class Meta:
		model = Userdata
		fields = {
			#'rankings',
		}
		
"""
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
	interests = fields_for_model(Userdata, ['interests'])['interests']
	
class ProjectForm(ModelForm):
	class Meta:
		model = Project
		fields = (
			'title',
			'description',
			'open',
			'url',
		)
	
	
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