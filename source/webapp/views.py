from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.views.generic import View, TemplateView
from django.utils.timezone import make_naive

from webapp.models import Goal, Status, Type
from webapp.forms import GoalForm


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


class GoalCreateView(View):
    def get(self, request):
        return render(request, 'goal_create.html', context={
            'form': GoalForm()
        })

    def post(self, request):
        form = GoalForm(data=request.POST)
        if form.is_valid():
            data = {}
            for key, value in form.cleaned_data.items():
                if value is not None:
                    data[key] = value
            goal = Goal.objects.create(**data)
            return redirect('goal_view', pk=goal.pk)
        else:
            return render(request, 'goal_create.html', context={
                'form': form
            })


class GoalUpdateView(TemplateView):
    template_name = 'goal_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        goal = get_object_or_404(Goal, pk=pk)

        initial = {}
        for key in 'summary', 'description', 'status', 'type':
            initial[key] = getattr(goal, key)
        initial['created_at'] = make_naive(goal.created_at).strftime('%Y-%m-%dT%H:%M')
        form = GoalForm(initial=initial)

        context['goal'] = goal
        context['form'] = form

        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        goal = get_object_or_404(Goal, pk=pk)
        form = GoalForm(data=request.POST)
        if form.is_valid():
            for key, value in form.cleaned_data.items():
                if value is not None:
                    setattr(goal, key, value)
            goal.save()
            return redirect('goal_view', pk=goal.pk)
        else:
            return self.render_to_response({
                'goal': goal,
                'form': form
            })


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
