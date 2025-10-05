from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from .models import Task
from django.db import connection
from django.core.exceptions import ValidationError


# View functions
def index(request):
	# checks whether user is authenticated
	if request.user.is_authenticated:
		# gets all tasks from the database
		task_list = Task.objects.filter(user=request.user) 
		# creates a dictionary to pass this list to the template file
		template_data = {'tasks': task_list}
		# renders the web page
		return render(request, 'index.html', template_data)
	else:
		return HttpResponseRedirect(reverse(f'login'))

# Adds a new task and redirect it back to index page
def add(request):
	if request.user.is_authenticated:
		# if the form was submitted
		if request.POST:
			title = request.POST['title']
			due_date = request.POST['due_date']
			status = request.POST['status']
			task = Task(user = request.user, title = title, due_date = due_date, status = status)
			# does input validation (full_clean() throws an exception if validation fails)
			try:
				task.full_clean() 
				# if no exception was thrown, form was validated
				# we proceed to save the task in the database using Django ORM
				# FIX: Replaced vulnerable raw SQL with Django ORM to prevent SQL injection
				# Django ORM automatically sanitizes inputs and uses parameterized queries
				task.save()
			except ValidationError as e:
				# renders the web page again with an error message
				return render(request, 'add.html', {"errors": e.message_dict})
				
			return HttpResponseRedirect(reverse(f'tasktracker:index'))
		else:
			# renders the web page
			return render(request, 'add.html')
	else:
		return HttpResponseRedirect(reverse(f'login'))


# Deletes a task (based on its primary key) and redirect it back to index page
def delete(request, pk):
	# FIX: Added authorization check to prevent IDOR vulnerability
	# Only allow users to delete their own tasks
	if request.user.is_authenticated:
		try:
			# Filter by both ID and user to ensure ownership
			task = Task.objects.get(id=pk, user=request.user)
			task.delete()
		except Task.DoesNotExist:
			# Task doesn't exist or doesn't belong to the user
			# Redirect to index without deletion
			pass
	# redirects user to index page
	return HttpResponseRedirect(reverse(f'tasktracker:index'))