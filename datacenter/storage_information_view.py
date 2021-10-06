from django.shortcuts import render
from django.utils.timezone import localtime as lt

from datacenter.models import Visit
from datacenter.models import get_duration
from datacenter.models import format_duration
from datacenter.models import is_visit_long


def storage_information_view(request):
    non_closed_visits = []
    active_visits = Visit.objects.filter(leaved_at=None)
    for visit in active_visits:
        duration_in_seconds = get_duration(visit)
        curent_visiter = {
                'who_entered': visit.passcard,
                'entered_at': lt(visit.entered_at).strftime('%d-%m-%y %H:%M'),
                'duration': format_duration(duration_in_seconds),
                'is_strange': is_visit_long(visit, minutes=60)
        }
        non_closed_visits.append(curent_visiter)

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
