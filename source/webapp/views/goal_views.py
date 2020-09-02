from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from webapp.models import Goal, Project
from webapp.forms import GoalForm


class GoalView(LoginRequiredMixin, DetailView):
    template_name = 'goal/goal_view.html'
    model = Goal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GoalCreateView(LoginRequiredMixin, CreateView):
    model = Goal
    template_name = 'goal/goal_create.html'
    form_class = GoalForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        goal = form.save(commit=False)
        goal.project = project
        goal.save()
        form.save_m2m()
        return redirect('project_view', pk=project.pk)


class GoalUpdateView(LoginRequiredMixin, UpdateView):
    model = Goal
    template_name = 'goal/goal_update.html'
    form_class = GoalForm

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.project.pk})


class GoalDeleteView(LoginRequiredMixin, DeleteView):
    model = Goal

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.project.pk})
