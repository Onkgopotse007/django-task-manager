# middleware.py

from django.shortcuts import redirect
from django.urls import reverse


class RedirectLoggedInUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                # Allow superuser to access admin pages
                if not request.path.startswith(reverse('admin:index')):
                    return redirect('admin:index')
            else:
                # Prevent access to other routes for non-superusers
                if request.path == reverse('login') or request.path == reverse('signup'):
                    return redirect('task_list')
        else:
            # Prevent access to other routes for anonymous users
            if request.path != reverse('login') and request.path != reverse('signup'):
                return redirect('login')
        response = self.get_response(request)
        return response
