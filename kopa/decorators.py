from django.shortcuts import redirect

def login_required(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            print("User is not authenticated. Redirecting to login.")
            return redirect('login')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
    

