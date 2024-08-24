from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone   


# Create your views here.
"""
def helloword (request):
    #return HttpResponse ('Hello Word!!')
    #title = 'Django'
    return render (request, 'signup.html',{
        #'mytitle': title
        'form': UserCreationForm
    })
"""
def home(request):
    return render (request, 'home.html')

def signup(request):
    if request.method == 'GET':
        print ('enviando formulario de datos (GET)')
        return render (request, 'signup.html',{
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # registrar usuario
                user = User.objects.create_user(
                username = request.POST['username'],
                password = request.POST['password1'])
                user.save()
                #return HttpResponse('Usuario creado exitosamente')
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                #return HttpResponse('Usuario ya existe')
                return render (request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'Usuario ya existe'
                })
           

        return render (request, 'signup.html',{
                    'form': UserCreationForm,
                    'error': 'contraseñas no coinciden'
                }) 

def tasks(request):
    #tasks = Task.objects.all()
    #tasks = Task.objects.filter(user = request.user)
    #tasks = Task.objects.filter(user = request.user, datecompleted__isnull = True)
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull = True)
    return render (request, 'tasks.html',{
        'tasks': tasks
    })

def tasks_completed(request):
    tasks = Task.objects.filter(user = request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render (request, 'tasks.html',{
        'tasks': tasks
    })

def create_task(request):
    if request.method == 'GET':
        return render (request, 'create_task.html',{
            'form': TaskForm
        })
    else:

        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render (request, 'create_task.html',{
                'form': TaskForm,
                'error': 'Por favor ingrese datos validos'
            })

def task_detail(request, task_id):
    #task = Task.objects.get(pk = task_id)
    if request.method == 'GET':
        task = get_object_or_404(Task, pk = task_id, user = request.user)
        form = TaskForm(instance = task)
        return render (request, 'task_detail.html',{
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk = task_id, user = request.user)
            form = TaskForm(request.POST,instance = task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render (request, 'task_detail.html',{
            'task': task,
            'form': form,
            'error': 'Error actualizando tarea'
            })

def complete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk = task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render (request, 'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render (request, 'signin.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('tasks')

        
    