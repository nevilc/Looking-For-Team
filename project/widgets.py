from django.forms.widgets import HiddenInput

class RankingWidget(HiddenInput):
	is_hidden = False

	def __init__(self, off_img_url='/static/nostar.png', on_img_url='/static/star.png', count=5, attrs=None):
		super(RankingWidget, self).__init__(attrs)
		self.count = count
		self.off_img_url = off_img_url
		self.on_img_url = on_img_url
		
	def action(self, id, name, number):
		return u"document.getElementById(\"" + id + u"\").value = \"" + str(number) + u"\";"
		
	def button(self, id, name, number):
		return u" <img src='" + self.off_img_url + u"' id='" + id + u'_' + str(number) + "' onClick='" + self.action(id, name, number) + "' />"
		
	def recursive_buttons(self, id, name, number):
		if number <= 0:
			return u""
			
		return self.recursive_buttons(id, name, number - 1) + self.button(id, name, number)
		
	def all_buttons(self, id, name):
		return self.recursive_buttons(id, name, self.count)
	
	def render(self, name, value, attrs=None):
		#name = str(name)
		id = u"id_" + name # hackish, there should be some way of getting id automatically
		return super(RankingWidget, self).render(name, value, attrs) + self.all_buttons(id, name)
	
	"""
	def render(self, name, value, attrs=None):
		#currently inits as zero no matter what
		
		# the field dictionary uses the skill id as a string for the key for easy skill lookup later
		# for whatever reason, name gets converted to int here, so make sure to use str(name)
		name = str(name)
		id = u"id_" + name
		
		if value == None:
			value = 0
			
		
		return u"<input type='hidden' id='" + id + u"' name='" + name + u"' value='" + str(value) + u"' />" + self.all_buttons(id, name)
	"""