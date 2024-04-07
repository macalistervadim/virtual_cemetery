import django.shortcuts


def home(request):
    template = "homepage/home.html"
    return django.shortcuts.render(request, template)