from django import forms
from .models import Goal, Status, Type


class GoalForm(forms.Form):
    summary = forms.CharField(max_length=200, required=True, label='Заголовок')
    description = forms.CharField(max_length=300, required=False, label='Описание', widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), required=True, label='Статус')
    type = forms.ModelChoiceField(queryset=Type.objects.all(), required=True, label='Тип')
