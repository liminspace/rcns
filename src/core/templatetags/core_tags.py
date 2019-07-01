from django import template
from django.utils.safestring import mark_safe


register = template.Library()


# @register.inclusion_tag('core/tags/show_messages.html', takes_context=True)
# def show_messages(context):
#     return context


# @register.inclusion_tag('core/tags/form_field_errors.html')
# def form_field_errors(errors):
#     return {'errors': errors}


# @register.inclusion_tag('core/tags/form_errors.html')
# def form_errors(form):
#     return {'errors': form.errors.get('__all__')}


@register.simple_tag(takes_context=True)
def assign(context, var_name, val=None, g=False):
    """
    Assign value to variable.
    g: set a global variable
    Example:
        {% assign 'var_name' 'value' %}
    """
    if callable(val):
        val = val()
    if g:
        context.dicts[0][var_name] = val
    else:
        context[var_name] = val
    return ''


@register.simple_tag(takes_context=True)
def assign_default(context, var_name, default=None, g=False):
    """
    Assign default value to variable if it does not exist.
    g: set a global variable
    Example:
        {% assign_default 'var_name' 'default_value' %}
    """
    if callable(default):
        default = default()
    if var_name not in context:
        if g:
            context.dicts[0][var_name] = default
        else:
            context[var_name] = default
    return ''


# _json_script_escapes = {
#     ord('>'): '\\u003E',
#     ord('<'): '\\u003C',
#     ord('&'): '\\u0026',
# }


# @register.filter
# def safe_js(js_str):
#     """
#     Make your js code safe.
#
#     Example:
#         obj = json.dumps({'a': '</script>'})
#
#         <script>
#             var myvar = {{ obj|safe_js }};
#         </script>
#     """
#     return mark_safe(str(js_str).translate(_json_script_escapes))


# @register.filter
# def strequal(val1, val2):
#     return str(val1) == str(val2)
