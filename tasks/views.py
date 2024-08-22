from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
                return HttpResponse('Usuario creado exitosamente')
            except:
                return HttpResponse('Usuario ya existe')
           

        return HttpResponse('Password no coincide')    

        
        
