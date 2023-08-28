from celery import shared_task
from django.db.models import Q

from code_review.models import File, StatusType, Log
from code_review.services import LintersService


@shared_task
def code_check():
    files = File.objects.filter(
        Q(status=StatusType.NEW)
        |
        Q(status=StatusType.MODIFIED)
    ).all()

    result = LintersService.check_files(files)
    for log in result:
        instance = Log.objects.filter(
            linter=log['linter'],
            file_id=log['file_id'],
            user_id=log['user_id']
        ).first()
        if instance:
            for field, value in log.items():
                setattr(instance, field, value)
            instance.save()
        else:
            instance = Log.objects.create(**log)

        File.objects.filter(id=instance.file_id).update(status=StatusType.CHECKED)

    return result


@shared_task
def send_email():
    pass
