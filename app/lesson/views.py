from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Task, Comment
from .forms import ProjectForm, TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('project_list')
    else:
        form = UserCreationForm()
    return render(request, 'lesson/registration.html', {'form': form})

@login_required
def project_list(request):
    projects = Project.objects.filter(members=request.user)
    return render(request, 'lesson/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            project.members.add(request.user)
            return redirect('projects_list')
    else:
        form = ProjectForm()
        return render(request, 'lesson/project_form.html', {'form': form})

@login_required   
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'lesson/project_detail.html', {'project':project})

@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects_list')
    return render(request, 'lesson/project_confirm_delete.html', {'project':project})

@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)
        return render(request, 'lesson/project_form.html', {'form':form})

@login_required
def project_add_members(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        user = User.objects.get(username=request.POST['username'])
        project.members.add(user)
        return redirect('project_detail', pk=pk)
    users = User.objects.exclude(id__in=project.members.all())
    return render(request, 'lesson/project_add_member.html', {'users': users, 'project': project})

@login_required
def project_delete_members(request, project_pk, user_pk):
    project = get_object_or_404(Project, pk=project_pk)
    user = get_object_or_404(User, pk=user_pk)
    if request.method == 'POST':
        project.members.remove(user)
        return redirect('project_detail', pk=project_pk)
    return render(request, 'lesson/members_delete_confirm.html', {'project': project, 'user': user})

@login_required
def task_create(request, project_pk):
    project = get_object_or_404(Project, pk=project_pk)
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm()
        return render(request, 'lesson/task_form.html', {'form': form, 'project': project})
    
@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'lesson/task_detail.html', {'task': task})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project = task.project
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('project_detail', pk=task.project.pk)
    else:
        form = TaskForm(instance=task)
        return render(request, 'lesson/task_form.html', {'form':form, 'project': project})
    
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    project_pk = task.project.pk
    if request.method == 'POST':
        task.delete()
        return redirect('project_detail', pk=project_pk)
    return render(request, 'lesson/task_confirm_delete.html', {'task': task})
