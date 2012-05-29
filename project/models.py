from django.db import models
from django.core import validators

class Tag(models.Model):
	title = models.CharField(max_length=24)
	
	def __unicode__(self):
		return self.title

class Project(models.Model):
	title = models.CharField(max_length=64, unique=True)
	description = models.TextField(max_length=1024)
	
	creation_date = models.DateTimeField('created')
	update_date = models.DateTimeField('last updated')
	
	open = models.BooleanField(default=True)
	
	project_url = models.URLField(max_length=200, blank=True)
	
	tags = models.ManyToManyField(Tag)
	
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
	
	project = models.ForeignKey(Project)
	
	def __unicode__(self):
		return self.title

class Skill(models.Model):
	title = models.CharField(max_length=24)
	description = models.TextField(max_length=1024)
	
	icon = models.ImageField(upload_to='icons')
	
	def __unicode__(self):
		return self.title
	
class Ranking(models.Model):
	value_range = (1, 5)

	skill = models.ForeignKey(Skill)
	
	rank = models.IntegerField(validators=[validators.MinValueValidator(value_range[0]), validators.MaxValueValidator(value_range[1])])
	
	# only used for Position rankings, can be left false for User skills
	# if true, the requirement /must/ be met to be returned as a match
	strict = models.BooleanField(default=False)
	
	position = models.ForeignKey(Position)
	
	def __unicode__(self):
		return '*' * self.rank

	

	
	