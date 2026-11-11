from django.shortcuts import render, redirect, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .forms import TaskForm
from .models import Task

# READ + CREATE
def task_list(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    tasks = Task.objects.all()
    return render(request, "app/task_list.html", {"tasks": tasks, "form": form})

# UPDATE: tick / untick
@require_POST
def toggle_task(request, id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=id)
        task.completed = not task.completed
        task.save()
    return redirect("task_list")

# UPDATE: edit title
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_list")
    else:
        form = TaskForm(instance=task)
    return render(request, "app/edit_list.html", {"form": form, "task": task})

# DELETE
@require_POST
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)
    task.delete()
    return redirect("task_list")