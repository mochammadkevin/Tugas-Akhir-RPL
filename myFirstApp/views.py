from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.utils.timezone import now
from .models import Task
from .models import Quote
from .models import Gratitude
from .models import Habit
from .models import Profile
from .models import Expense
from django.contrib import messages
import random

@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    quotes = Quote.objects.all()
    quote = random.choice(quotes)
    habit = Habit.objects.filter(user=request.user).order_by('?').first() # This retrieves a random habit from the database
    tasks = Task.objects.filter(user=request.user)
    context = { 'profile': profile, 'quote': quote, 'tasks': tasks }

    if habit is not None:
        context['habit_title'] = habit.title
        context['habit_emoji'] = habit.emoji
        context['habit_description'] = habit.description

    if request.method == 'POST':
        desc = request.POST['desc']
        created = now()
        gratitude = Gratitude.objects.create(user=request.user, desc=desc, created=created)
        return redirect('gratitude_journal')

    return render(request, 'index.html', context)




@login_required
def habit(request):
    habits = Habit.objects.filter(user=request.user)
    return render(request, 'habit.html', {'habits': habits})

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

@login_required
def gratitude(request):
    return render(request, 'gratitude.html')

@login_required
def gratitudecreate(request):
   if request.method == 'POST':
        desc = request.POST['desc']
        created = now()
        gratitude = Gratitude.objects.create(user=request.user, desc=desc, created=created)
        if 'from_index' in request.POST:
            return redirect('index')
        else:
            return redirect('gratitude_journal')
   return render(request, 'gratitude_create.html')

@login_required
def gratitudejournal(request):
    gratitudes = Gratitude.objects.filter(user=request.user)
    context = {
        'gratitudes': gratitudes
    }
    return render(request, 'gratitude_journal.html', context)

@login_required
def gratitudedelete(request, pk):
    gratitude = Gratitude.objects.get(pk=pk, user=request.user)
    gratitude.delete()
    return redirect('gratitude_journal')

@login_required
def settingsedit(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.username = request.POST['username']
        user.email = request.POST['email']

        if request.POST.get('change_password') == 'on':
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']

            if user.check_password(current_password):
                if new_password == confirm_password:
                    user.set_password(new_password)
                else:
                    messages.error(request, 'New password and confirm password do not match.')
                    return redirect('settingsedit')
            else:
                messages.error(request, 'Current password is incorrect.')
                return redirect('settingsedit')

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('settings')
    return render(request, 'settingsedit.html')

@login_required
def habitcreate(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        emoji = request.POST['emoji']
        monday = request.POST.get('monday', False)
        tuesday = request.POST.get('tuesday', False)
        wednesday = request.POST.get('wednesday', False)
        thursday = request.POST.get('thursday', False)
        friday = request.POST.get('friday', False)
        saturday = request.POST.get('saturday', False)
        sunday = request.POST.get('sunday', False)
        habit = Habit.objects.create(user=request.user, title=title, description=description, emoji=emoji)
        habit.save()
        return redirect('habit')
    return render(request, 'habit_create.html')

@login_required
def habitupdate(request, id):
    habit = Habit.objects.get(id=id)
    if request.method == 'POST':
        habit.monday = 'monday' in request.POST
        habit.tuesday = 'tuesday' in request.POST
        habit.wednesday = 'wednesday' in request.POST
        habit.thursday = 'thursday' in request.POST
        habit.friday = 'friday' in request.POST
        habit.saturday = 'saturday' in request.POST
        habit.sunday = 'sunday' in request.POST
        habit.save()
        return redirect('habit')
    return render(request, 'habit_update.html', {'habit': habit})

@login_required
def habitdelete(request, id):
    habit = Habit.objects.get(id=id)
    habit.delete()
    return redirect('habit')

@login_required
def habitdetail(request, id):
    habit = Habit.objects.get(id=id)
    context = {
        'habit': habit
    }
    return render(request, 'habit_detail.html', context)


@login_required
def habit_edit(request, id):
    habit = Habit.objects.get(id=id)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        emoji = request.POST['emoji']
        habit.title = title # Update the habit object with the new values
        habit.description = description
        habit.emoji = emoji
        habit.save()
        return redirect('habit')
    return render(request, 'habit_edit.html', {'habit': habit})

@login_required
def financetracker(request):
    profile = Profile.objects.filter(user=request.user).first()
    expenses = Expense.objects.filter(user=request.user)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        amount = request.POST.get('amount')
        expense_type = request.POST.get('expense_type')

        expense = Expense(name=text, amount=amount, expense_type=expense_type, user=request.user)
        expense.save()
        
        if expense_type == 'Positive':
            if profile.balance is None:
                profile.balance = float(amount)
            else:
                profile.balance += float(amount)
            profile.income += float(amount)
        else:
            if profile.balance is None:
                profile.balance = 0 - float(amount)
            else:
                profile.expenses += float(amount)
                profile.balance -= float(amount)
            
        profile.save()
        return redirect('financetracker')

    context = {'profile': profile, 'expenses': expenses}
    return render(request, 'financetracker.html', context)





