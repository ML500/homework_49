from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView

from webapp.models import Goal, Project
from webapp.forms import GoalForm


class ProjectGoalCreateView(CreateView):
    model = Goal
    template_name = 'goal/goal_create.html'
    form_class = GoalForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        goal = form.save(commit=False)
        goal.project = project
        goal.save()
        return redirect('project_view', pk=project.pk)
