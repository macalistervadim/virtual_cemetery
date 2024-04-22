import django.contrib.auth.forms
import django.core
import django.forms

import core.forms
import feedback.models


class MultipleFileInput(django.forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(django.forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class FeedbackFormFiles(
    core.forms.BootstrapFormMixin,
    django.forms.ModelForm,
):
    """
    Дополнительные файлы для формы обратной связи
    """

    files = MultipleFileField(required=False)

    class Meta:
        model = feedback.models.FeedbackFiles
        fields = ("files",)


class FeedbackForm(
    core.forms.BootstrapFormMixin,
    django.forms.ModelForm,
):
    class Meta:
        model = feedback.models.Feedback
        fields = (
            feedback.models.Feedback.text.field.name,
            feedback.models.Feedback.theme.field.name,
        )
