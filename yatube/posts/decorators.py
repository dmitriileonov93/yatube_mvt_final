from functools import wraps

from django.shortcuts import redirect


def only_author(func):
    @wraps(func)
    def check_user(request, *args, **kwargs):
        if request.user.username in kwargs['username']:
            return func(request, *args, **kwargs)
        return redirect('post', *args, **kwargs)
    return check_user
