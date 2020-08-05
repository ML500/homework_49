from django import forms
from .models import Goal, Status, Type


class GoalForm(forms.Form):
    summary = forms.CharField(max_length=200, required=True, label='Заголовок')
    description = forms.CharField(max_length=300, required=False, label='Описание', widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True,
                                    initial=Status.objects.first(), label='Статус')
    type = forms.ModelChoiceField(queryset=Type.objects.all(),
                                  initial=Type.objects.first(), required=True, label='Тип')
    created_at = forms.DateTimeField(required=False, label='Время публикации',
                                     input_formats=['%Y-%m-%d', '%Y-%m-%dT%H:%M', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M',
                                                    '%Y-%m-%d %H:%M:%S'],
                                     widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
