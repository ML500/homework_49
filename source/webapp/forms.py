from django import forms
from django.forms import DateInput

from .models import Goal, Project


class FengyuanChenDatePickerInput(DateInput):
    template_name = 'widgets/fengyuanchen_datepicker.html'


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
        widgets = {'start_date': FengyuanChenDatePickerInput,
                   'end_date': FengyuanChenDatePickerInput}
