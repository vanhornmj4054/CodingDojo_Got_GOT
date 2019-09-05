from __future__ import unicode_literals
from django.db import models
from datetime import date
from django.utils.dateparse import parse_date
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class LoginManager(models.Manager):
	def user_validator(self, postData):
		errors = {}
		if len(postData['first_name']) < 3:
			errors["first_name"] = "First name must be at least 2 characters"
		if len(postData["last_name"]) < 3:
			errors["last_name"] = "Last name must be at least 2 characters"
		if len(postData["password"]) < 8:
			errors["password_len"] = "Password must be at least 8 characters"
		if not re.match("(?=.*[a-z])(?=.*[A-Z])(?=.*\W)", postData["password"]):
		if postData["password"] != postData["password_confirm"]:
			errors["password"] = "Passwords do not match"

		user = User.objects.filter(email=postData['email'])
		if len(user) != 0:
			errors["login_password"] = "This email has already been registered"

		if not EMAIL_REGEX.match(postData['email']):
			errors["login_email"] = "invalid user email"
		return errors

	def event_validator(self, postData):
		errors = {}
		today = date.today()
		created_at = postData["when"]
		created_date = parse_date(created_at)
		
		if len(postData['title']) < 3:
			errors['title'] = "This event requires a title"
		if postData['genre'] == "select":
			errors['genre'] = "Genre field required"
		if created_date == None:
			errors['when'] = "Must enter a date"
		elif created_date < today:
			errors['when'] = "Must select a date in the future"

		return errors
				

class User(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField(max_length=45)
	password = models.CharField(max_length=20)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = LoginManager()


class Event(models.Model):
	title = models.CharField(max_length=45)
	genre = models.CharField(max_length=45)
	location = models.CharField(max_length=45)
	time_date = models.DateTimeField(auto_now=False)
	created_by = models.ForeignKey(User, related_name="events_hosting")
	attendees = models.ManyToManyField(User, related_name="events_attending")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = LoginManager()

	


