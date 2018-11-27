from django import template

register = template.Library()


def pagination(value, offset):
    current_page_number = value.number
    lower = current_page_number - offset
    higher = current_page_number + offset

    if lower < 0:
        lower = 0
        higher = offset + offset

    return "{0}:{1}".format(lower, higher)


register.filter('pagination_offset', pagination)
