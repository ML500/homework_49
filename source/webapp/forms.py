from django import forms
from .models import Goal, Status, Type


class GoalForm(forms.Form):
    summary = forms.CharField(max_length=200, required=True, label='Заголовок')
    description = forms.CharField(max_length=300, required=False, label='Описание', widget=forms.Textarea)
    status = forms.ModelChoiceField(queryset=Status.objects.all(), initial=0, required=True, label='Статус')
    type = forms.ModelMultipleChoiceField(queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple,
                                          required=False, label='Тип')
