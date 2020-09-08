from django import template
from django.conf import settings


register = template.Library()


@register.filter
def page_query_string(request, page_number):
    query_args = request.GET.copy()
    query_args['page'] = page_number
    return query_args.urlencode()


@register.filter
def display_page(page_obj, num):
    num_end = settings.PAGINATION.get('end_pages', 3)
    num_side = settings.PAGINATION.get('round_pages', 2)
    last = page_obj.paginator.num_pages
    current = page_obj.number
    page_obj.show_prev = getattr(page_obj, 'show_this', None)
    page_obj.show_this = num <= num_end or num > last - num_end \
                         or current - num_side <= num <= current + num_side
    return page_obj.show_this
