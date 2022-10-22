from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import Room, Topic, Message

from .forms import RoomForm, UserFrom

# Create your views here.


def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]

    room_count = rooms.count()

    roomMessages = Message.objects.filter(Q(room__topic__name__icontains=q))

    return render(request, 'base/home.html', {
        'rooms': rooms,
        'topics': topics,
        'room_count': room_count,
        'roomMessages': roomMessages
    })


def room(request, pk):

    roomDetail = Room.objects.get(pk=pk)
    roomMessages = roomDetail.message_set.all().order_by('-created')
    participants = roomDetail.participants.all()

    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=roomDetail,
            body=request.POST.get('body'),
        )
        roomDetail.participants.add(request.user)

        return redirect('room', roomDetail.id)

    return render(request, 'base/room.html', {
        'room': roomDetail,
        'roomMessages': roomMessages,
        'participants': participants
    })


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(pk=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {
        'obj': message
    })


def useProfile(request, pk):
    user = User.objects.get(pk=pk)

    rooms = user.room_set.all()
    roomMessage = user.message_set.all()
    topics = Topic.objects.all()
    return render(request, 'base/profile.html', {
        'user': user,
        'rooms': rooms,
        'roomMessage': roomMessage,
        'topics': topics,
    })


@login_required(login_url='login')
def createRoom(request):

    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    return render(request, 'base/room_form.html', {
        'form': form,
        'topics': topics,
    })


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(pk=pk)

    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')

        topic, created = Topic.objects.get_or_create(name=topic_name)

        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    return render(request, 'base/room_form.html', {
        'form': form,
        'topics': topics,
        'room': room
    })


def deleteRoom(request, pk):

    room = Room.objects.get(pk=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {
        'obj': room
    })


def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user doet not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'username and password is not exist')

    return render(request, 'base/login_register.html', {
        'page': page
    })


def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'ann error occurred during registertion')

    return render(request, 'base/login_register.html', {
        'form': form
    })


def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserFrom(instance=user)

    if request.method == 'POST':
        form = UserFrom(request.POST, instance=user)

        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {
        'form': form,
    })


def topicPage(request):
    q = request.GET.get('q') if request.GET.get('q') else ''

    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {
        'topics': topics
    })


def activitiesPage(request):

    roomMessages = Message.objects.all()

    return render(request, 'base/activity.html', {
        'roomMessages': roomMessages,
    })
