from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import *
from .forms import*

# Create your views here.

def LoginPage(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user=User.objects.get(email=email)
        except:
            messages.error(request,'USER NOT FOUND')

        user=authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'EMAIL OR PASSWORD DOESNOT EXIST')    
    context={'page':page}
    return render(request,'pannel/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')    

def RegisterUser(request):
    
    form=MyUserCreationform()
    if request.method=='POST':
        form=MyUserCreationform(request.POST)
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
    topics=Topic.objects.all()[0:5]
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms,'topics':topics,'room_count':room_count,'room_messages':room_messages}
    return render (request,'pannel/home.html',context) 

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all()
    participant=room.participant.all()

    if request.method =='POST':
        message=Message.objects.create(user=request.user,room=room,body=request.POST.get('body'))
        room.participant.add(request.user)
        return redirect('room',pk=room.id)

    context={'room':room,'room_messages':room_messages,'participant':participant}         
    return render (request,'pannel/room.html',context) 

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={'user':user,
    'rooms':rooms,
    'room_messages':room_messages,
    'topics':topics

    }
    return render(request,'pannel/profile.html',context)


@login_required(login_url='login')
def Create_room(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method =="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        # form=RoomForm(request.POST)
        # if form.is_valid():
        #     room=form.save(commit=False)
        #     room.host=request.user
        #     room.save()
        return redirect('home')    
    context={'form':form,'topic':topics}
    return render(request,'pannel/room_form.html',context)    

@login_required(login_url='login')
def UpdateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()

    if request.user!=room.host:
        return HttpResponse('Virus')
    if request.method =="POST":
        topic_name=request.POST.get('topic')
        topic,created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()

        
        return redirect('home')
    context={'form':form,'topic':topics,'room':room}
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


@login_required(login_url='login')
def Update_profile(request):
    user=request.user
    form=Updateuser(instance=user)
    if request.method=='POST':
        form=Updateuser(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    context={
        'form':form
    }
    return render(request,'pannel/update-user.html',context)  


def topics(request):
    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    topics=Topic.objects.filter(name__icontains=q)
    context={'topics':topics}
    return render(request,'pannel/topics.html',context)    

def activity(request):
    room_messages=Message.objects.all()
    context={'room_messages':room_messages}
    return render(request,'pannel/activity.html',context)     