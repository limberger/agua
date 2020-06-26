from django.urls import path, register_converter

from . import views, converters

register_converter(converters.MonthYearConverter, 'mmyyyy')

app_name = 'agua'
urlpatterns = [
    path('', views.agua_list, name='agua_list'),
    path('new', views.agua_create, name='agua_new'),
    path('view/<int:pk>', views.agua_view, name="agua_view"),
    path('edit/<int:pk>', views.agua_update, name="agua_edit"),
    path('delete/<int:pk>', views.agua_delete, name="agua_delete"),
    path('demonstrativo', views.demonstrativo, name="demonstrativo"),
    path('demonstrativo/<mmyyyy:competencia>/', views.demonstrativo, name="demonstrativo"),

]
