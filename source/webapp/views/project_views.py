from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView

from accounts.admin import User
from webapp.models import Project
from webapp.forms import SimpleSearchForm, ProjectForm, GoalForm, UserForm
from webapp.views.base_views import SearchView
from django.contrib.auth import get_user_model


class IndexView(LoginRequiredMixin, SearchView):
    template_name = 'project/index.html'
    context_object_name = 'projects'
    model = Project
    paginate_by = 5
    search_form = SimpleSearchForm

    def get_query(self, search):
        query = Q(name__icontains=search) | \
                Q(description__icontains=search)
        return query


@login_required
def project_mass_action_view(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_projects', [])
        if 'delete' in request.POST:
            Project.objects.filter(id__in=ids).delete()
    return redirect('webapp:index')


class ProjectView(LoginRequiredMixin, DetailView):
    model = Project
    template_name = 'project/project_view.html'
    paginate_by = 5


class ProjectCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'project/project_create.html'
    form_class = ProjectForm
    model = Project
    permission_required = 'webapp.add_project'

    def form_valid(self, form):
        user = self.request.user
        users = get_user_model().objects.filter(pk=user.pk)
        project = form.save(commit=False)
        project.save()
        project.user.set(users)
        return redirect('webapp:project_view', pk=project.pk)


class ProjectUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'project/project_update.html'
    form_class = ProjectForm
    model = Project
    permission_required = 'webapp.change_project'

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})


class ProjectDeleteView(PermissionRequiredMixin, DeleteView):
    model = Project
    template_name = 'project/project_delete.html'
    success_url = reverse_lazy('webapp:index')
    permission_required = 'webapp.delete_project'


class UserAddView(PermissionRequiredMixin, UpdateView):
    model = Project
    form_class = UserForm
    template_name = 'project/add_user.html'
    permission_required = 'auth.add_user'

    def has_permission(self):
        self.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().has_permission() and self.request.user in self.project.user.all()

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs.get('pk'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['project'] = self.project
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        return reverse('webapp:project_view', kwargs={'pk': self.object.pk})





