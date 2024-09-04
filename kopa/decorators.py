from django.shortcuts import redirect
from django.contrib import messages

def login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Sorry, please login first to be able to access the form")
            return redirect('login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
    

