from sqlite3 import IntegrityError

from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import  login,logout,authenticate
from django.utils import timezone

from .forms import TodoForm
from .models import Todo
from django.contrib.auth.decorators import login_required
# Create your views here.

def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password2'])
                user.save()
                login(request=request,user=user)
                return redirect('currenttoddos')
            except IntegrityError :
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'Username already exist'})

        else:
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(),'error':'error password dismatch'})


@login_required
def currenttoddos(request):
    todos=Todo.objects.filter(user=request.user,datecompleted__isnull=True)
    return render(request,'todo/currenttoddos.html',{'todos':todos})

@login_required

def viewtodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk,user=request.user)

    if request.method=="GET" :
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo': todo , 'form':form})
    else :
        try:
            form=TodoForm(request.POST,instance=todo)
            form.save()
            return redirect("currenttoddos")
        except ValueError :
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form , "error":"Bad entry data"})


def logoutt(request):
    if request.method=='POST':
        logout(request)
        return redirect('home')
    else:
        return redirect('home')


def home(request):
    return render(request,'todo/home.html')

def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo/login.html', {'form': AuthenticationForm()})
    else:
        user=authenticate(request,password=request.POST['password'],username=request.POST['username'])
        if user is None :
            return render(request, 'todo/login.html', {'form': AuthenticationForm(),'error':"Mot de Pass ou username Incorrect"})
        else:
            login(request,user)
            return redirect("currenttoddos")

@login_required
def createtodo(request):
    if request.method == "GET":
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})


    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect("currenttoddos")
        except ValueError :
            return render(request, 'todo/createtodo.html', {'form': TodoForm(),'error':"Fields filling error"})

@login_required

def completetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

    if request.method=="POST":
        todo.datecompleted=timezone.now()
        todo.save()
        return redirect("currenttoddos")


def deletetodo(request,todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)

    if request.method == "POST":
        todo.delete()
        return redirect("currenttoddos")






def listcompleted(request):
    todoscompleted=Todo.objects.filter(datecompleted__isnull=False)
    return render(request,'todo/listcompleted.html',{'todoscompleted':todoscompleted})
