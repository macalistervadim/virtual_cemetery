import django.contrib.auth.forms
import django.core
import django.forms

import core.forms
import event.models


class EventWorkRegister(
    core.forms.BootstrapFormMixin,
    django.forms.ModelForm,
):
    """
    Форма регистрации участника конкурса
    """

    class Meta:
        model = event.models.WorkUser
        exclude = (event.models.WorkUser.user.field.name,)


class VoteWorkEvent(
    core.forms.BootstrapFormMixin,
    django.forms.ModelForm,
):
    """
    Форма для оценки текущей работы
    """

    class Meta:
        model = event.models.VoteEvent
        fields = (event.models.VoteEvent.score.field.name,)
