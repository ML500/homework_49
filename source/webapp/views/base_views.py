from django.views.generic import View, ListView
from django.shortcuts import render, redirect


class FormView(View):
    form_class = None
    template_name = None
    redirect_url = ''

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        return redirect(self.get_redirect_url())

    def form_invalid(self, form):
        context = self.get_context_data(form=form)
        return render(self.request, self.template_name, context=context)

    def get_context_data(self, **kwargs):
        return kwargs

    def get_redirect_url(self):
        return self.redirect_url


class SearchView(ListView):
    template_name = None
    context_object_name = None
    model = None
    search_form = None

    def get_context_data(self, *, object_list=None, **kwargs):
        form = self.search_form(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        kwargs['form'] = form
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = self.model.objects.filter(is_deleted=False)
        form = self.search_form(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(self.get_query(search))
        return data

    def get_query(self, search):
        query = None
        return query

