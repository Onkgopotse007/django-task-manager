from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .forms import TaskForm
from .models import Task


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')


def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})


def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})


def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})


def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})


def task_listboard(request):
    # Retrieve all users for the dropdown menu
    all_users = User.objects.all()

    # Retrieve tasks for the current user
    tasks = Task.objects.filter(user=request.user)

    # Apply user filtering
    user_filter = request.GET.get('user')
    if user_filter and user_filter.isdigit():
        tasks = tasks.filter(user_id=user_filter)

    # Sorting
    sort_by = request.GET.get('sort_by')
    if sort_by == 'name':
        tasks = tasks.order_by('name')
    elif sort_by == 'due_date':
        tasks = tasks.order_by('due_date')

    # Filtering by completion status
    completion_filter = request.GET.get('completion')
    if completion_filter in ['true', 'false']:
        tasks = tasks.filter(completion=(completion_filter == 'true'))

    return render(request, 'task_listboard.html', {'tasks': tasks, 'all_users': all_users})
