from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView, ListView
from django.db.models import Q
from django.utils.timezone import make_naive

from webapp.models import Goal, Status, Type
from webapp.forms import GoalForm, SimpleSearchForm


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'goals'
    paginate_by = 3
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        kwargs['form'] = form
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Goal.objects.all()

        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(summary__icontains=search) | Q(description__icontains=search))

        return data.order_by('-created_at')


class GoalView(TemplateView):
    template_name = 'goal_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        goal = get_object_or_404(Goal, pk=pk)

        context['goal'] = goal
        return context


class GoalCreateView(FormView):
    template_name = 'goal_create.html'
    form_class = GoalForm

    def form_valid(self, form):
        self.goal = form.save()
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
