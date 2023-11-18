from django import template
from django.utils.safestring import mark_safe
from menu_app.models import MenuItem
from django.urls import reverse

register = template.Library()

def fetch_submenu(menu_item):
    return MenuItem.objects.filter(parent=menu_item)

@register.simple_tag
def draw_menu(menu_name, current_path):
    root_items = MenuItem.objects.filter(parent=None)
    print(root_items)
    if not root_items:
        return "Menu not found."

    result = """<div class="collapse navbar-collapse" id="navbarNav"><ul class="navbar-nav">"""
    for root_item in root_items:
        is_active = current_path == root_item.url
        result += f"""<li class='nav-item {'active' if is_active else ''}'><a class='nav-link' href='{root_item.url}'>{root_item.title}</a></li>"""

        # Fetch and draw submenu
        submenu_items = fetch_submenu(root_item)
        if submenu_items:
            result += draw_submenu(submenu_items, current_path)

    result += """</ul></div>"""
    return mark_safe(result)

def draw_submenu(menu_items, current_path):
    result = "<div class='collapse navbar-collapse' id='navbarNav'><ul class='nav'>"
    for item in menu_items:
        is_active = current_path.startswith(item.url)
        result += f"""<li class='nav-item {'active' if is_active else ''}'><a class='nav-link' href='{item.url}'>{item.title}</a></li>"""

        # Fetch and draw submenu
        submenu_items = fetch_submenu(item)
        if submenu_items:
            result += draw_submenu(submenu_items, current_path)

    result += "</ul>"
    return result