from django import forms
from .models import Goal, Status, Type


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['summary', 'description', 'status', 'type']
        widgets = {'type': forms.CheckboxSelectMultiple}
