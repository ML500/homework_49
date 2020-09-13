from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.urls import reverse

from accounts.forms import MyUserCreationForm
from django.views.generic import CreateView, DetailView, ListView

from accounts.models import Profile


class RegisterView(CreateView):
    model = User
    template_name = 'user_create.html'
    form_class = MyUserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('index')
        return next_url

    # def register_view(request, *args, **kwargs):


#     if request.method == 'POST':
#         form = MyUserCreationForm(data=request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             return redirect('webapp:index')
#     else:
#         form = MyUserCreationForm()
#     return render(request, 'user_create.html', context={'form': form})


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'
    # paginate_related_by = 5
    # paginate_related_orphans = 0


class UserView(PermissionRequiredMixin, ListView):
    model = User
    template_name = 'user_view.html'
    context_object_name = 'users'
    permission_required = 'auth.view_user'
