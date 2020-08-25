from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from webapp.models import Project
from webapp.forms import SimpleSearchForm, ProjectForm
from webapp.views.base_views import SearchView


class IndexView(SearchView):
    template_name = 'project/index.html'
    context_object_name = 'projects'
    model = Project
    paginate_by = 3
    paginate_orphans = 0
    search_form = SimpleSearchForm

    def get_query(self, search):
        query = Q(name__icontains=search) | \
                Q(description__icontains=search)
        return query


def project_mass_action_view(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_projects', [])
        if 'delete' in request.POST:
            Project.objects.filter(id__in=ids).delete()
    return redirect('index')


class ProjectView(DetailView):
    template_name = 'project/project_view.html'
    model = Project
    paginate_goals_by = 4
    paginate_orphans = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        goals, page, is_paginated = self.paginate_goals(self.object)
        context['goals'] = goals
        context['page_obj'] = page
        context['is_paginated'] = is_paginated  # page.has_other_pages()

        return context

    def paginate_goals(self, project):
        goals = project.goals.all().order_by('-created_at')
        if goals.count() > 0:
            paginator = Paginator(goals, self.paginate_goals_by, orphans=self.paginate_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1
            return page.object_list, page, is_paginated
        else:
            return goals, None, False


class ProjectCreateView(CreateView):
    template_name = 'project/project_create.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectUpdateView(UpdateView):
    template_name = 'project/project_update.html'
    form_class = ProjectForm
    model = Project

    def get_success_url(self):
        return reverse('project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(DeleteView):
    template_name = 'project/project_delete.html'
    model = Project
    success_url = reverse_lazy('index')

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
