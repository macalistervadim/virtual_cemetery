import django.contrib
import django.shortcuts
import django.utils.translation as translation

import feedback.forms
import feedback.models


@django.contrib.auth.decorators.login_required
def feedback_view(request):
    template = "feedback/feedback.html"
    user = request.user

    try:
        existing_feedback = feedback.models.Feedback.objects.get(user=user)
    except feedback.models.Feedback.DoesNotExist:
        existing_feedback = None

    if request.method == "POST":
        form = feedback.forms.FeedbackForm(request.POST)
        form_files = feedback.forms.FeedbackFormFiles(request.POST, request.FILES)
        if existing_feedback:
            django.contrib.messages.error(
                request,
                translation.gettext_lazy(
                    "У вас уже есть активное обращение. Вы не можете создать еще одно.",
                ),
            )
        else:
            if form.is_valid():
                feedback_instance = form.save(commit=False)
                feedback_instance.user = user
                feedback_instance.save()

                for uploaded_file in request.FILES.getlist("files"):
                    feedback.models.FeedbackFiles.objects.create(
                        feedback=feedback_instance, files=uploaded_file,
                    )

                django.contrib.messages.success(
                    request,
                    translation.gettext_lazy(
                        "Обратная связь отправлена. Ожидайте ответа на почту.",
                    ),
                )
                return django.shortcuts.redirect("feedback:feedback")
    else:
        form = feedback.forms.FeedbackForm()
        form_files = feedback.forms.FeedbackFormFiles()

    context = {"form": form, "form_files": form_files}

    return django.shortcuts.render(request, template, context)
