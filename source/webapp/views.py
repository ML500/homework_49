from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from django.views.generic import View, TemplateView, FormView
from django.utils.timezone import make_naive

from webapp.models import Goal, Status, Type
from webapp.forms import GoalForm
from .base_views import FormView as CustomFormView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        goal = Goal.objects.all()

        context['goals'] = goal
        return context


class GoalView(TemplateView):
    template_name = 'goal_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        goal = get_object_or_404(Goal, pk=pk)

        context['goal'] = goal
        return context


# class GoalCreateView(CustomFormView):
#     template_name = 'goal_create.html'
#     form_class = GoalForm
#
#     def form_valid(self, form):
#         data = {}
#         type = form.cleaned_data.pop('type')
#         for key, value in form.cleaned_data.items():
#             if value is not None:
#                 data[key] = value
#         self.goal = Goal.objects.create(**data)
#         self.goal.type.set(type)
#         return super().form_valid(form)
#
#     def get_redirect_url(self):
#         return reverse('goal_view', kwargs={'pk': self.goal.pk})

class GoalCreateView(FormView):
    template_name = 'goal_create.html'
    form_class = GoalForm

    def form_valid(self, form):
        data = {}
        type = form.cleaned_data.pop('type')
        for key, value in form.cleaned_data.items():
            if value is not None:
                data[key] = value
        self.goal= Goal.objects.create(**data)
        self.goal.type.set(type)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('goal_view', kwargs={'pk': self.goal.pk})


class GoalUpdateView(FormView):
    template_name = 'goal_update.html'
    form_class = GoalForm

    def dispatch(self, request, *args, **kwargs):
        self.goal = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goal'] = self.get_object()
        return context

    def get_initial(self):
        initial = {}
        for key in 'summary', 'description', 'status':
            initial[key] = getattr(self.goal, key)
        initial['created_at'] = make_naive(self.goal.created_at).strftime('%Y-%m-%dT%H:%M')
        initial['type'] = self.goal.type.all()
        return initial

    def form_valid(self, form):
        type = form.cleaned_data.pop('type')
        for key, value in form.cleaned_data.items():
            if value is not None:
                setattr(self.goal, key, value)
        self.goal.save()
        self.goal.type.set(type)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('goal_view', kwargs={'pk': self.goal.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Goal, pk=pk)


class GoalDeleteView(TemplateView):
    template_name = 'goal_delete.html'

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

        return redirect('index')
