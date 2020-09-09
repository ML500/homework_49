from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


class GoalCreateView(PermissionRequiredMixin, CreateView):
    model = Goal
    form_class = GoalForm
    template_name = 'goal/goal_create.html'
    permission_required = 'webapp.add_goal'

    def has_permission(self):
        self.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in self.project.user.all()

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['project'] = self.project
        kwargs['user'] = self.request.user
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.instance.project = self.project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project.pk})

    # def form_valid(self, form):
    #     project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
    #     goal = form.save(commit=False)
    #     goal.project = project
    #     goal.save()
    #     form.save_m2m()
    #     return redirect('webapp:project_view', pk=project.pk)


class GoalUpdateView(PermissionRequiredMixin, UpdateView):
    model = Goal
    template_name = 'goal/goal_update.html'
    form_class = GoalForm
    permission_required = 'webapp.change_goal'

    def has_permission(self):
        goal = self.get_object()
        return super().has_permission() and self.request.user in goal.project.user.all()

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project.pk})


class GoalDeleteView(PermissionRequiredMixin, DeleteView):
    model = Goal
    template_name = 'goal/goal_delete.html'
    permission_required = 'webapp.delete_goal'

    def has_permission(self):
        goal = self.get_object()
        return super().has_permission() and self.request.user in goal.project.user.all()

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.project.pk})
