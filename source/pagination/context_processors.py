from django.conf import settings


def page_display_modes(request):
    display_modes = settings.PAGINATION.get('pages_display', ['page_list'])
    context = {'pages_display': {}}
    for mode in display_modes:
        context['pages_display'][mode] = True
    return context
