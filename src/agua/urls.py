from django.urls import path

from . import views

app_name = 'agua'
urlpatterns = [
    path('', views.agua_list, name='agua_list'),
    path('new', views.agua_create, name='agua_new'),
    path('view/<int:pk>', views.agua_view, name="agua_view"),
    path('edit/<int:pk>', views.agua_update, name="agua_edit"),
    path('delete/<int:pk>', views.agua_delete, name="agua_delete"),

]
