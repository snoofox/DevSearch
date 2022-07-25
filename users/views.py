from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .helpers import searchProfiles, paginateProfiles


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.GET.get('next', False) == "/reset_password_sent/":
        messages.info(
            request, "We've emailed you instructions for setting your password, if an account exists with the email you entered. You should recieve them shortly.")

    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, "Username or Password is incorrect")
    return render(request, 'users/auth.html', context={'page': 'login'})


def logoutUser(request):
    logout(request)
    messages.info(request, "User was logged out!")
    return redirect('login')


def registerUser(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "User account was created!")
            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request, "An error has occurred")
    return render(request, "users/auth.html", context={'page': 'signup', 'form': CustomUserCreationForm()})


def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request, profiles, 6)
    context = {'profiles': profiles, 'search_query': search_query,
               'custom_range': custom_range}
    return render(request, 'users/profiles.html', context=context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")
    context = {'profile': profile, 'topSkills': topSkills,
               'otherSkills': otherSkills}
    return render(request, 'users/user-profile.html', context=context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    context = {'profile': profile, 'skills': profile.skill_set.all(),
               'projects': profile.project_set.all()}
    return render(request, 'users/account.html', context=context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    return render(request, 'users/profile_form.html', {'form': ProfileForm(instance=profile)})


@login_required(login_url='login')
def createSkill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.admin = request.user.profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect('account')

    return render(request, 'users/skill_form.html', context={'form': SkillForm()})


@login_required(login_url='login')
def updateSkill(request, pk):
    skill = request.user.profile.skill_set.get(id=pk)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect('account')

    return render(request, 'users/skill_form.html', context={'form': SkillForm(instance=skill)})


def deleteSkill(request, pk):
    skill = request.user.profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect('account')
    return render(request, 'delete.html', {'object': skill})


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequests = profile.messages.all()
    unreadCount = messageRequests.filter(is_read=False).count()
    context = {'messageRequests': messageRequests, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if not message.is_read:
        message.is_read = True
        message.save()

    context = {'message': message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recepient = Profile.objects.get(id=pk)
    if request.method == "POST":
        if request.user.is_authenticated:
            sender = request.user.profile
        else:
            sender = None

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipent = recepient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            return redirect('user-profile', pk=recepient.id)
    context = {'recipient': recepient, 'form': MessageForm()}
    return render(request, 'users/message_form.html', context)
