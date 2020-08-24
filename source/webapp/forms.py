from django import forms
from .models import Goal, Status, Type, Project
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['summary', 'description', 'status', 'type']
        widgets = {'type': forms.CheckboxSelectMultiple}


class SimpleSearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label="Найти")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date']



