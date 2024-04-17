import django.shortcuts

import faq.models


def faq_view(request):
    template = "faq/faq.html"

    faq_list = faq.models.FaqQuestions.objects.get_faq_list()

    context = {
        "faq_list": faq_list,
    }

    return django.shortcuts.render(request, template, context)
