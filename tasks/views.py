from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

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
    return render (request, 'tasks.html')        
        
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

        
    