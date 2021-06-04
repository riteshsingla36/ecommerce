from django.shortcuts import redirect, render

def unauthoriseduser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'customer':
            return redirect('home')
        
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
        
        else:
            return redirect('loginpage')

    return wrapper_func