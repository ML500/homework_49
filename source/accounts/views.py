from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse

from accounts.forms import MyUserCreationForm
from django.views.generic import CreateView


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
