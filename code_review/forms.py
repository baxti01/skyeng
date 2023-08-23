from datetime import timedelta

from django import forms
from django.core.validators import FileExtensionValidator

PERIOD_CHOICES = [
    (timedelta(minutes=1), 'minute'),
    (timedelta(hours=1), 'hour'),
    (timedelta(days=1), 'day'),
    (timedelta(weeks=1), 'week'),
]


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        attrs = kwargs.pop('attrs', None)
        kwargs.setdefault("widget", MultipleFileInput(attrs=attrs))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class UploadFileForm(forms.Form):
    files = MultipleFileField(
        attrs={'accept': '.py'},
        validators=[
            FileExtensionValidator(allowed_extensions=['py'])
        ]
    )
    start_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    period = forms.ChoiceField(choices=PERIOD_CHOICES)


class ModifyForm(forms.Form):
    file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'accept': '.py'}),
        validators=[
            FileExtensionValidator(allowed_extensions=['py'])
        ]
    )
    start_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    period = forms.ChoiceField(choices=PERIOD_CHOICES)
