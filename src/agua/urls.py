from django.urls import path

from . import views

app_name = 'core'
urlpatterns = [
    path('', views.familia_list, name='familia_list'),
    path('new', views.familia_create, name='familia_new'),
    path('view/<int:pk>', views.familia_view, name="familia_view"),
    path('edit/<int:pk>', views.familia_update, name="familia_edit"),
    path('delete/<int:pk>', views.familia_delete, name="familia_delete"),

]
