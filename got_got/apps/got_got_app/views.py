from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):
	request.session["id"] = None #<------ sets any logged in user to NONE to facilitate log out
	return render(request, "got_got_app/index.html")

def register(request):
	first_name = request.POST["first_name"]
	last_name = request.POST["last_name"]
	email = request.POST["email"]
	password = request.POST["password"]
	pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) #<------------- encodes and salts password

	errors = User.objects.user_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		request.session["id"] = None
		return redirect("/")
	else:
		user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash)
		request.session["id"] = user.id
		return redirect("/dashboard")


def login(request):
	user = User.objects.get(email=request.POST['login_email'])
	password = request.POST['login_password']
	pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 

	if bcrypt.checkpw(password.encode(), user.password.encode()): #<------------ checks encoded entered password
		request.session["id"] = user.id #<------------------------------ if match, set user id into session
		return redirect("/dashboard") #<------------------------------------ and send to books page
	else:
		return redirect("/") # <------------ if not a match, redirect back to login page


def dashboard(request):
	if request.session["id"] == None: #<------------------- prevents unauthorized access, maybe?
		return redirect('/')
	else:
		user = User.objects.get(id=request.session["id"])
		events = Event.objects.all()
		# event = Event.objects.get(id=id)


		context = {
			"user" : user,
			"events": events,
			"host_count": len(user.events_hosting.all()),
			"joined_count": len(user.events_attending.all()),
			# "event": event,
		}

	return render(request, "got_got_app/dashboard.html", context)


def create(request):
	# title = request.POST["title"]
	# genre = request.POST["genre"]
	# when = request.POST["when"]
	# location = request.POST["location"]
	# event = Event.objects.create(title=title, genre=genre, time_date=when, location=location)

	return render(request, "got_got_app/new_event.html")


def add_event(request):
	title = request.POST["title"]
	genre = request.POST["genre"]
	when = request.POST["when"]
	location = request.POST["location"]
	user = User.objects.get(id=request.session["id"])

	errors = User.objects.event_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/create")
	else:
		event = Event.objects.create(title=title, genre=genre, time_date=when, location=location, created_by=user)
		user.events_attending.add(event)
		return redirect("/dashboard")


def events(request):
	if request.session["id"] == None: #<------------------- prevents unauthorized access, maybe?
		return redirect('/')
	else:
		user = User.objects.get(id=request.session["id"])
		# event = Event.objects.get(id=id)
		context = {
			"user" : user,
			"upcoming_events": Event.objects.all(),
		}

		return render(request, "got_got_app/events.html", context)


def view_event(request, id):
	user = User.objects.get(id=request.session["id"])
	event = Event.objects.get(id=id)

	context = {
		"user": user,
		"event": event,
	}

	return render(request, "got_got_app/view_event.html", context)

def cancel_event(request, id):
	# user = User.objects.get(id=request.session["id"])
	event = Event.objects.get(id=id)
	event.delete()

	return redirect("/events")


def join_event(request, id):
	user = User.objects.get(id=request.session["id"])
	event = Event.objects.get(id=id)
	event.attendees.add(user)

	return redirect(f"/view_event/{event.id}")










