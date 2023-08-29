from django import template

from code_review.models import StatusType, SentStatusType

register = template.Library()


@register.inclusion_tag('code_review/get_file_status.html')
def get_file_status(file):
    statuses = []
    if file.status == StatusType.NEW:
        statuses.append(
            {
                'icon_path': 'code_review/images/not_checked.svg',
                'tooltip': 'Файл ещё не проверен'
            }
        )

    if file.status == StatusType.MODIFIED:
        statuses.append(
            {
                'icon_path': 'code_review/images/edited.svg',
                'tooltip': 'Файл изменён'
            }
        )

    if file.status == StatusType.FAILED:
        statuses.append(
            {
                'icon_path': 'code_review/images/x.svg',
                'tooltip': 'Ошибка проверки файла'
            }
        )

    if file.status == StatusType.CHECKED:
        statuses.append(
            {
                'icon_path': 'code_review/images/checked.svg',
                'tooltip': 'Файл проверен'
            }
        )

    return {'statuses': statuses}


@register.inclusion_tag('code_review/notification_status.html')
def get_notification_status(sent_status):
    status = {
        'icon_path': 'code_review/images/x.svg',
        'tooltip': 'Уведомление ещё не отправлено'
    }

    if sent_status == SentStatusType.SENT:
        status['icon_path'] = 'code_review/images/checked.svg'
        status['tooltip'] = 'Уведомление отправлено'

    return {'status': status}
