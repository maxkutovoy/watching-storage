from django.db import models
from django.utils.timezone import localtime as lt


def get_duration(visit):
    if visit.leaved_at:
        finish_time = lt(visit.leaved_at)
    else:
        finish_time = lt()
    start_time = lt(visit.entered_at)
    duration_in_seconds = (finish_time - start_time).total_seconds()
    return duration_in_seconds


def format_duration(duration_in_seconds):
    duration_in_hours = duration_in_seconds // 3600
    duration_in_minutes = (duration_in_seconds % 3600) // 60
    return "{:02.0f} час. {:02.0f} мин.".format(
        duration_in_hours,
        duration_in_minutes,
    )


def is_visit_long(visit, minutes=60):
    suspicious_activity_time = minutes * 60
    return get_duration(visit) > suspicious_activity_time


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= 'leaved at ' + str(self.leaved_at) if self.leaved_at else 'not leaved'
        )
