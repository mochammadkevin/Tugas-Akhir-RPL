from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Task
from .models import Quote
import random


@login_required
def index(request):
    quotes = Quote.objects.all()
    quote = random.choice(quotes)
    context = {
        'quote': quote
    }
    return render(request, 'index.html', context)

@login_required
def habit(request):
    return render(request, 'habit.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            email = request.POST['email']
            first_name = request.POST['first_name']
            user.email = email
            user.first_name = first_name
            user.save()
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'register.html')
    elif request.method == 'GET':
        return render(request, 'register.html')

def loginview(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html')

    elif request.method == 'GET':
        return render(request, 'login.html')

def logoutview(request):
    logout(request)
    return redirect('index')

@login_required
def tasklist(request):
    print(request.user)
    tasks = Task.objects.filter(user=request.user)
    context = {
        'tasks': tasks
    }
    return render(request, 'task_list.html', context)

@login_required
def taskdetail(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    context = {
        'task': task
    }
    return render(request, 'task_detail.html', context)

@login_required
def taskcreate(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        deadline = request.POST['deadline']
        task = Task.objects.create(user=request.user, title=title, description=description, deadline=deadline)
        return redirect('tasks')
    return render(request, 'task_create.html')

@login_required
def taskdelete(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    task.delete()
    return redirect('tasks')

@login_required
def taskcomplete(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if task.complete:
        task.complete = False
    else:
        task.complete = True
    task.save()
    return redirect('tasks')

@login_required
def taskupdate(request, pk):
    task = Task.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.deadline = request.POST['deadline']
        task.save()
        return redirect('tasks')
    context = {
        'task': task
    }
    return render(request, 'task_update.html', context)

@login_required
def settings(request):
    if request.method == 'POST':
        user = request.user
        user.profile.image = request.FILES['profile']
        user.profile.save()
        return redirect('settings')
    return render(request, 'settings.html')

