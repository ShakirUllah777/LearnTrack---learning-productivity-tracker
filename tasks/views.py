from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Task
from .forms import TaskForm

@login_required
def task_list(request):
    query = request.GET.get('q', '').strip()
    priority_filter = request.GET.get('priority', '').strip()
    status_filter = request.GET.get('status', '').strip()

    tasks = Task.objects.filter(user=request.user)

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    form = TaskForm()
    context = {
        'tasks': tasks,
        'form': form,
        'query': query,
        'priority_filter': priority_filter,
        'status_filter': status_filter,
        'active_tab': 'tasks',
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, f"Task '{task.title}' created successfully!")
        else:
            messages.error(request, "Failed to create task. Please check the form fields.")
    return redirect('task_list')


@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f"Task '{task.title}' updated successfully!")
            return redirect('task_list')
        else:
            messages.error(request, "Failed to update task. Please check the form errors.")
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_edit.html', {'form': form, 'task': task, 'active_tab': 'tasks'})


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        title = task.title
        task.delete()
        messages.success(request, f"Task '{title}' deleted.")
    return redirect('task_list')


@login_required
def task_toggle(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if task.status == 'COMPLETED':
        task.status = 'PENDING'
    else:
        task.status = 'COMPLETED'
    task.save()
    messages.success(request, f"Status updated for '{task.title}'.")
    return redirect(request.META.get('HTTP_REFERER', 'task_list'))
