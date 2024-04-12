__all__ = ["LoadUserMiddleware"]

import users.models


class LoadUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.id:
            request.user = users.models.User.objects.get(pk=request.user.id)

        return self.get_response(request)
