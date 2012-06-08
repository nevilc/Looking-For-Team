from django.forms import ModelForm

from project.models import Userdata
from django.contrib.auth.models import User

class UserForm(ModelForm):
	class Meta:
		model = User
		#exclude = (

class UserdataForm(ModelForm):
	class Meta:
		model = Userdata
		exclude = (
			'user',
			
		)