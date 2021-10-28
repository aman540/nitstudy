from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import *
from .forms import*

# Create your views here.

def LoginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'USER NOT FOUND')

        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'USERNAME OR PASSWORD DOESNOT EXIST')    
    context={'page':page}
    return render(request,'pannel/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')    

def RegisterUser(request):
    
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'error occur in reqistreation')
    context={'form':form}
    return render(request,'pannel/login_register.html',context)

def index(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    rooms=Room.objects.filter(Q(topic__name__icontains=q)|Q(name__icontains=q)|Q(description__icontains=q))
    room_count=rooms.count()
    topics=Topic.objects.all()
    context={'rooms':rooms,'topics':topics,'room_count':room_count}
    return render (request,'pannel/home.html',context) 

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participant=room.participant.all()

    if request.method =='POST':
        message=Message.objects.create(user=request.user,room=room,body=request.POST.get('body'))
        room.participant.add(request.user)
        return redirect('room',pk=room.id)

    context={'room':room,'room_messages':room_messages,'participant':participant}         
    return render (request,'pannel/room.html',context) 

@login_required(login_url='login')
def Create_room(request):
    form=RoomForm()
    if request.method =="POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')    
    context={'form':form}
    return render(request,'pannel/room_form.html',context)    

@login_required(login_url='login')
def UpdateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)

    if request.user!=room.host:
        return HttpResponse('Virus')
    if request.method =="POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'pannel/room_form.html',context)    



@login_required(login_url='login')
def DeleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user!=room.host:
        return HttpResponse('Virus')

    if request.method =='POST':
        room.delete()
        return redirect('home')  
    return render(request,'pannel/delete.html',{'obj':room})


@login_required(login_url='login')
def DeleteMessage(request,pk):
    message=Message.objects.get(id=pk)
    if request.user!=message.user:
        return HttpResponse('Virus')

    if request.method =='POST':
        message.delete()
        return redirect('home')  
    return render(request,'pannel/delete.html',{'obj':message})        