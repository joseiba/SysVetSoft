from django.urls import path, re_path
from django.contrib.auth.decorators import login_required

from app import views

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    re_path(r'^.*\.html', views.gentella_html, name='gentella'),

    # The home page
    path('', login_required(views.index), name='index'),
]
