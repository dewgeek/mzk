from django.db import models
from django.contrib.auth.models import User
import os

class location(models.Model):
	name = models.CharField(max_length=50)
	
	def __unicode__(self):
	        return self.name

class food_type(models.Model):  #veg || Nonveg
	name = models.CharField(max_length = 20)	
	def __unicode__(self):
	        return self.name

class food_level(models.Model):  #veg || Nonveg
	name = models.CharField(max_length = 20)	
	def __unicode__(self):
	        return self.name

class food_course(models.Model): 
	name = 	models.CharField(max_length = 20)
	def __unicode__(self):
	    return u'%s' %(self.name)

class food_delivery(models.Model):
	name = models.ForeignKey(food_course)
	start_time = models.TimeField()
	end_time = models.TimeField()
	def __unicode__(self):
		return u"%s %s %s" %(self.name, self.start_time, self.end_time)

class pic_category(models.Model):
	name = models.CharField(max_length=20)
	def __unicode__(self):
			return self.name

class price_list(models.Model):
	course = models.ForeignKey(food_course)
	level = models.ForeignKey(food_level)
	foodtype = models.ForeignKey(food_type)
	cost = models.IntegerField(max_length=10)
	def __unicode__(self):
		return u"%s, %s, %s, %s" %(self.course,self.level,self.foodtype,self.cost)

def get_file_path(instance, filename):

	ext = filename.split('.')[-1]
	try:
		top_level = kitchen_data.objects.all().order_by("-id")[0]
		top_level = top_level.id + 1

	except:
		top_level = 1	
	
	filename = "%s.%s" % ("profile", ext)
	pic_path = str(top_level)+"/profile/"
	return os.path.join(pic_path, filename)

class kitchen_data(models.Model):
	name = models.CharField(max_length=50)
	#city = models.ForeignKey(city)
	spec_location = models.ForeignKey(location)
	description = models.TextField(max_length = 500)		
	profile = models.FileField(upload_to=get_file_path)
	pop_food = models.TextField(max_length = 100)
	
	foodlevel = models.ForeignKey(food_level)
	foodtype = models.ForeignKey(food_type)
	fooddelivery = models.ManyToManyField(food_delivery)
	time_stamp = models.DateTimeField(auto_now_add=True)	
	
	def __unicode__(self):
	        return u'%s' %(self.name)

class user_data(models.Model):
	user_object = models.OneToOneField(User) 
	mobile = models.TextField(max_length=20)
	status = models.BooleanField(default=True)
	def __unicode__(self):
		return u'%s' %(self.name)		

class orders(models.Model):
	user = models.ForeignKey(User)
	kitchen = models.ForeignKey(kitchen_data)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	course = models.ForeignKey(food_course)
	mobile = models.TextField(max_length=100)
	address = models.TextField(max_length=100)
	landmark = models.TextField(max_length=50)
	quantity = models.IntegerField(default=1)
	is_active = models.BooleanField(default = True)
	def __unicode__(self):
		return u'%s %s' %(self.user, self.course)		

class crumb_data(models.Model):			#cancelled, #Increased #Changed Address
	name=models.CharField(max_length=20)
	def __unicode__(self):
		return u'%s' %(self.name)		

class calender(models.Model):
	date = models.IntegerField(max_length=2)
	month = models.IntegerField(max_length=2)
	year = models.IntegerField(default=2014)
	day = models.TextField(max_length=10)
	def __unicode__(self):
		return u'%s %s %s %s' %(self.date, self.month, self.year, self.day)		

class crumbs(models.Model):
	order = models.ForeignKey(orders)
	options = models.ForeignKey(crumb_data)
	quantity = models.IntegerField(max_length=2,default=1)
	date = models.DateField(auto_now_add=False)
	mobile = models.TextField(max_length=100,null=True)
	address = models.TextField(max_length=100,null=True)
	landmark = models.TextField(max_length=50,null=True)
	time_stamp = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return u'%s %s' %(self.order, self.options)		

class pictures(models.Model):
	def some_stuff(instance,filename):
		path = str(instance.kitchen.id)+"/"+str(instance.pic_category)+"/"
		return os.path.join(path, filename)
	title = models.CharField(max_length=50)
	caption = models.TextField(max_length = 200)
	kitchen = models.ForeignKey(kitchen_data)
	pic_category = models.ForeignKey(pic_category) 
	photo = models.FileField(upload_to=some_stuff)
	extra_chars = models.CharField(max_length = 50,null = True,blank = True)
	display_as_main = models.BooleanField(default=False)
	time_stamp = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return u'%s' %(self.title)


class messages(models.Model):
	name = models.CharField(max_length=50)
	email = models.CharField(max_length=50,null=True)
	message = models.TextField(max_length = 500)
	def __unicode__(self):
	    return u'%s' %(self.name)

class reset_key(models.Model):
	user_object = models.OneToOneField(User) 
	key=models.CharField(max_length=100)
	def __unicode__(self):
	    return u'%s' %(self.user_object)