from django import template

register = template.Library()

@register.filter
def render_json(value):
    if isinstance(value, dict):
        return render_dict(value)
    elif isinstance(value, list):
        return render_list(value)
    else:
        return value

def render_dict(d):
    html = '<ul>'
    for key, value in d.items():
        html += f'<li><strong>{key}:</strong> {render_json(value)}</li>'
    html += '</ul>'
    return html

def render_list(lst):
    html = '<ul>'
    for item in lst:
        html += f'<li>{render_json(item)}</li>'
    html += '</ul>'
    return html
