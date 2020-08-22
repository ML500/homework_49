from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, FormView

from webapp.models import Goal
from webapp.forms import GoalForm, SimpleSearchForm
from webapp.views.base_views import SearchView


class IndexView(SearchView):
    template_name = 'project/index.html'
    context_object_name = 'goals'
    model = Goal
    paginate_by = 3
    paginate_orphans = 0
    search_form = SimpleSearchForm

    def get_query(self, search):
        query = Q(summary__icontains=search) | \
                Q(description__icontains=search)
        return query


class GoalView(TemplateView):
    template_name = 'project/project_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        goal = get_object_or_404(Goal, pk=pk)

        context['goal'] = goal
        return context


class GoalCreateView(FormView):
    template_name = 'project/project_create.html'
    form_class = GoalForm

    def form_valid(self, form):
        self.goal = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('goal_view', kwargs={'pk': self.goal.pk})


class GoalUpdateView(FormView):
    template_name = 'project/project_update.html'
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
    template_name = 'project/project_delete.html'

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
