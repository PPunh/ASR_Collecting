from django import template
from django.template.defaultfilters import floatformat
from django.urls import NoReverseMatch, Resolver404, resolve, reverse

register = template.Library()


@register.filter
def get_obj_attr(obj, attr_path):
    """Get attribute or dict key from object by path like 'customer_info.name' or 'customer_info__name'."""
    if not obj or not attr_path:
        return ""

    # convert from __ to . for nested attributes
    path = str(attr_path).replace("__", ".")

    for part in path.split("."):
        try:
            # 1. if Dictionary get from Key
            if isinstance(obj, dict):
                obj = obj.get(part)
            # 2. if Object get from Attribute
            else:
                obj = getattr(obj, part)

            # 3. Resault Method / Callable Function
            if callable(obj):
                obj = obj()

        except (AttributeError, TypeError, KeyError):
            return ""

    return obj if obj is not None else ""