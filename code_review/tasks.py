from celery import shared_task
from django.core.mail import BadHeaderError, send_mail
from django.db.models import Q

from code_review.models import File, StatusType, Log, SentStatusType
from code_review.services import LintersService
from skyeng import settings


@shared_task
def code_check_task():
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
        send_email_task.apply_async(
            kwargs={
                'linter': instance.linter,
                'file_id': instance.file_id,
                'user_id': instance.user_id,
                'email': instance.user.email,
            }
        )

    return result


@shared_task
def send_email_task(linter, file_id, user_id, email):
    subject = f'{linter.capitalize()}: Code review notification.'
    message = f'Your file is checked with {linter}. See more details in website'
    try:
        send_mail(
            subject=subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            message=message,
            recipient_list=[email]
        )
    except BadHeaderError:
        return 'Invalid header error'

    log = Log.objects.filter(
        linter=linter,
        file_id=file_id,
        user_id=user_id
    ).update(sent_status=SentStatusType.SENT)

    return log
