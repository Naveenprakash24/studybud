from django.shortcuts import render, redirect
from django.http import HttpResponse 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from .models import Room, Topic
from django.contrib.auth.models import User
from .forms import RoomForm




# rooms=[
#     {'id':1, 'name':"Hello from india"},
#     {'id':2, 'name':"Hello from USA"},
#     {'id':3, 'name':"Hello from China"},
#     {'id':4, 'name':"Hello from london"}
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist.')
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    context={'page':page}
    return render(request, 'baseApp/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    page= 'register'
    context={'page':page}
    return render(request, 'baseApp/login_register.html',context)


def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render(request, 'baseApp/home.html',context )

def room(request,pk):
    room=Room.objects.get(id=pk)
    context = {'room':room}
    return render(request, 'baseApp/room.html', context)


@login_required(login_url='login')
def createroom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context ={'form':form }
    return render(request, 'baseApp/room_form.html',context)



@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("Your are not allowed here!!")

    if request.method=='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request, 'baseApp/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room= Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("Your are not allowed here!!")
    if request.method=='POST':
        room.delete()
        return redirect('home')
    return render(request, 'baseApp/delete.html',{'obj':room})


