from django.shortcuts import render, redirect
from .forms import ProjectForm, ReviewForm
from .models import Project, Tag
from django.contrib.auth.decorators import login_required
from .utils import searchProjects, paginateProjects


def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProjects(request, projects, 6)

    context = {'projects': projects,
               'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context=context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.admin = request.user.profile
        review.save()
        projectObj.getVoteCount
        return redirect('project', pk=projectObj.id)

    return render(request, "projects/single-project.html", {'project': projectObj, 'form': ReviewForm()})


@login_required(login_url="login")
def createProject(request):
    if request.method == "POST":
        newTags = request.POST.get('newtags').replace(
            ',', ' ').replace('-', ' ').split(' ')
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.admin = request.user.profile
            project.save()

            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('projects')
    return render(request, "projects/project_form.html", {'form': ProjectForm()})


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        newTags = request.POST.get('newtags').replace(
            ',', ' ').replace('-', ' ').split(' ')
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    return render(request, "projects/project_form.html", {'form': ProjectForm(instance=project), 'project': project})


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('account')
    return render(request, 'delete.html', {'object': project})
