from django.shortcuts import render
from menu_app.models import MenuItem
from .templatetags.menu_tags import draw_submenu

def my_view(request):
    # print(draw_submenu.result)
    menu_data = MenuItem.objects.filter(parent=None)
    menus = MenuItem.objects.exclude(parent=None)
    print(menus)
    return render(request, 'menu.html', {'menu_data': menu_data, 'menus':menus})
