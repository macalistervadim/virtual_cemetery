import django.conf
import django.contrib
import django.contrib.auth.decorators
import django.shortcuts
import django.utils
import django.utils.translation as translation

import event.forms
import event.models


def all_events_view(request):
    template = "event/all_events.html"
    all_events = event.models.Event.objects.get_all_events()

    context = {
        "events": all_events,
    }

    return django.shortcuts.render(request, template, context)


def get_current_event_view(request, pk):
    template = "event/current_event.html"
    curr_event = event.models.Event.objects.get_current_event(pk=pk).first()
    curr_event_works = event.models.WorkUser.objects.get_current_event_works(pk=pk)

    context = {
        "event": curr_event,
        "works": curr_event_works,
    }

    return django.shortcuts.render(request, template, context)


@django.contrib.auth.decorators.login_required(login_url="users:login")
def registration_event_work(request):
    template = "event/register_event_work.html"

    if request.method == "POST":
        form = event.forms.EventWorkRegister(request.POST or None, request.FILES or None)
        if form.is_valid():
            try:
                pre_commit = form.save(commit=False)
                pre_commit.user = request.user
                pre_commit.save()
                django.contrib.messages.success(
                    request,
                    translation.gettext_lazy(
                        "Ваша работа успешно зарегистрирована. Ожидайте результатов конкурса",
                    ),
                )
                return django.shortcuts.redirect("event:all-events")
            except django.db.IntegrityError:
                django.contrib.messages.error(
                    request,
                    translation.gettext_lazy(
                        "Вы уже регистрировали вашу работу на данный конкурс. Повторая подача работы недоступна.",
                    ),
                )

    form = event.forms.EventWorkRegister()
    context = {"form": form}
    return django.shortcuts.render(request, template, context)


@django.contrib.auth.decorators.login_required(login_url="users:login")
def get_current_work_event(request, pk):
    """
    Просмотр конкретной работы
    """
    template = "event/current_work_event.html"
    get_work = event.models.WorkUser.objects.get_current_work(pk=pk)
    votes = event.models.VoteEvent.objects.filter(work=get_work)
    user_vote = votes.filter(user=request.user).first()
    average_rating = votes.aggregate(django.db.models.Avg("score"))["score__avg"]

    if request.method == "POST":
        form = event.forms.VoteWorkEvent(request.POST or None)
        if form.is_valid():
            pre_commit = form.save(commit=False)
            pre_commit.user = request.user
            pre_commit.work = event.models.WorkUser.objects.get(pk=pk)
            pre_commit.created_on = django.utils.timezone.now()
            if request.user == get_work.user:
                django.contrib.messages.error(
                    request,
                    translation.gettext_lazy(
                        "Вы не можете поставить оценку самому себе",
                    ),
                )
            else:
                if user_vote:
                    pre_commit.id = user_vote.id
                    pre_commit.save()
                else:
                    pre_commit.save()
                django.contrib.messages.success(
                    request,
                    translation.gettext_lazy(
                        "Оценка поставлена",
                    ),
                )
            return django.shortcuts.redirect("event:current-work", pk=pk)

    form = event.forms.VoteWorkEvent(instance=user_vote)

    context = {
        "work": get_work,
        "form": form,
        "votes": votes,
        "average_rating": average_rating,
    }

    return django.shortcuts.render(request, template, context)
