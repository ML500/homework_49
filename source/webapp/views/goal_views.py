from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView, FormView, TemplateView

from webapp.models import Goal, Project
from webapp.forms import GoalForm


class GoalView(DetailView):
    template_name = 'goal/goal_view.html'
    model = Goal

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class GoalCreateView(CreateView):
    model = Goal
    template_name = 'goal/goal_create.html'
    form_class = GoalForm

    def form_valid(self, form):
        project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        goal = form.save(commit=False)
        goal.project = project
        goal.save()
        return redirect('project_view', pk=project.pk)


class GoalUpdateView(FormView):
    template_name = 'goal/goal_update.html'
    form_class = GoalForm

    def dispatch(self, request, *args, **kwargs):
        self.goal = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal'] = self.get_object()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.goal
        return kwargs

    def form_valid(self, form):
        self.goal = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('goal_view', kwargs={'pk': self.goal.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Goal, pk=pk)


class GoalDeleteView(TemplateView):
    template_name = 'goal/goal_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        goal = get_object_or_404(Goal, pk=pk)

        context['goal'] = goal
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        goal = get_object_or_404(Goal, pk=pk)
        goal.delete()

        return redirect('project_view', goal.project.pk)
