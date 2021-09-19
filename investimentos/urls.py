from django.urls import path

from . import views

app_name = 'investimentos'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('adicionar_acao/', views.adicionar_acao, name='adicionar_acao'),
    path('importar/', views.importar_preferencias, name='importar'),
    path('exportar/', views.exportar_preferencias, name='exportar'),
    path('buscar_acao/', views.buscar_acao, name='buscar_acao')
]