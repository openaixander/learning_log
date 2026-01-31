from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def register(request):
    """ 
    Register a new user
    """

    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            # save the new user into the database
            new_user = form.save()


            # log them immediately
            login(request, new_user)

            return redirect('learning_logs:index')
    
    context = {
        'form':form
        }
    return render(request, 'registration/register.html', context)