from django.shortcuts import render
#from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def helloword (request):
    #return HttpResponse ('Hello Word!!')
    #title = 'Django'
    return render (request, 'signup.html',{
        #'mytitle': title
        'form': UserCreationForm
    })
