from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils.timezone import localtime as lt


from datacenter.models import format_duration
from datacenter.models import get_duration
from datacenter.models import is_visit_long
from datacenter.models import Passcard
from datacenter.models import Visit


def passcard_info_view(request, passcode):
    this_passcard_visits = []
    try:
        passcard = Passcard.objects.get(passcode=passcode)
    except Passcard.DoesNotExist:
        return "Сотрудник не найден"
    except Passcard.MultipleObjectsReturned:
        return "Найдено несолько сотрудников"
        
    passcard_visits = Visit.objects.filter(passcard=passcard)

    for visit in passcard_visits:
        duration_in_seconds = get_duration(visit)
        passcard_visits = {
                'entered_at': lt(visit.entered_at).strftime('%d-%m-%y %H:%M'),
                'duration': format_duration(duration_in_seconds),
                'is_strange': is_visit_long(visit, minutes=60)
            }
        this_passcard_visits.append(passcard_visits)

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
