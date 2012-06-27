from django.db import models
from django.core import validators

from django.contrib.contenttypes import generic

from django.contrib.auth.models import User

from django.contrib.contenttypes.models import ContentType

import time

class Tag(models.Model):
	title = models.CharField(max_length=24)
	
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	
	target = generic.GenericForeignKey('content_type', 'object_id')
	
	def __unicode__(self):
		return self.title

class Skill(models.Model):
	title = models.CharField(max_length=24)
	description = models.TextField(max_length=1024)
	
	icon = models.ImageField(upload_to='icons')
	
	parent = models.ForeignKey("self", blank=True, null=True)
	
	def __unicode__(self):
		return self.title
		
class Ranking(models.Model):
	value_range = (1, 5)

	skill = models.ForeignKey(Skill)
	
	rank = models.IntegerField(validators=[validators.MinValueValidator(value_range[0]), validators.MaxValueValidator(value_range[1])])
	
	# only used for Position rankings, can be left false for User skills
	# if true, the requirement /must/ be met to be returned as a match
	strict = models.BooleanField(default=False)
	
	#position = models.ForeignKey(Position)
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	
	target = generic.GenericForeignKey('content_type', 'object_id')
	
	def __unicode__(self):
		return '*' * self.rank
		
class Userdata(models.Model):
	@staticmethod
	def avatar_filename(instance, filename):
		return "avatar/" + instance.user.username + "_" + time.gmtime() + "_" + filename
	
	#user = models.ForeignKey(User, unique=True)
	user = models.OneToOneField(User)
	
	avatar = models.ImageField(upload_to=avatar_filename, blank=True)
	
	bio = models.TextField(max_length=1024, blank=True)
	
	url = models.URLField(max_length=200, blank=True)
	
	interests = generic.GenericRelation(Tag)
	rankings = generic.GenericRelation(Ranking)
	
	# location
	
	def __unicode__(self):
		return self.user.username
	
	
		
class Project(models.Model):
	title = models.CharField(max_length=64, unique=True)
	description = models.TextField(max_length=1024)
	
	creation_date = models.DateTimeField('created')
	update_date = models.DateTimeField('last updated')
	
	open = models.BooleanField(default=True)
	
	url = models.URLField(max_length=200, blank=True)
	
	#tags = models.ManyToManyField(Tag, blank=True)
	tags = generic.GenericRelation(Tag)
	
	#admins
	
	def __unicode__(self):
		return self.title
	
class Position(models.Model):
	title = models.CharField(max_length=64)
	description = models.TextField(max_length=1024)
	
	creation_date = models.DateTimeField('created')
	update_date = models.DateTimeField('last updated')
	
	# A restricted position requires a project admin to accept a user application
	# Any user can accept an open position
	restricted = models.BooleanField(default=True)
	
	# A repeating position can accept any number of users
	# For example, a volunteer open source project may be looking for any number of people to
	# work on bug fixes, etc.
	# Otherwise, the position will be removed from searches once it has been filled
	repeating = models.BooleanField(default=False)
	
	rankings = generic.GenericRelation(Ranking)
	
	project = models.ForeignKey(Project)
	
	def __unicode__(self):
		return self.title
		
class Invite(models.Model):
	position = models.ForeignKey(Position)
	
	message = models.TextField(max_length=1024)
	
	#sender = models.ForeignKey(User)
	#recipient = models.ForeignKey(User)

	read = models.BooleanField(default=False)
	
class Application(models.Model):
	position = models.ForeignKey(Position)
	
	message = models.TextField(max_length=1024)

	#sender = models.ForeignKey(User)
	
	read = models.BooleanField(default=False)
	
	accepted = models.NullBooleanField(default=None)