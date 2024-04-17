import django.shortcuts


def about_view(request):
    template = "about/about.html"

    return django.shortcuts.render(request, template)
