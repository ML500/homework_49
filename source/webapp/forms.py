from django import forms
from .models import Goal, Status, Type
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['summary', 'description', 'status', 'type']
        widgets = {'type': forms.CheckboxSelectMultiple}

    def clean_summary(self):
        summary = self.cleaned_data['summary']

        if not summary[0].isdigit():
            if ord(summary[0]) < 65 or ord(summary[0]) > 90:
                raise ValidationError('First letter not capital!')
        return summary


@deconstructible
class MaxLengthValidator(BaseValidator):
    message = 'Value "%(value)s" has length of %(show_value)d! ' \
              'It should be at least %(limit_value)d symbols long!'
    code = 'too_short'

    def compare(self, value, limit):
        return value > limit

    def clean(self, value):
        return len(value)
