from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_anuncios, name="listar_anuncios"),
    path('ver/<anuncio_id>', views.ver_anuncio, name="ver_anuncio"),
    path('filtros/tipo/<tipo_id>', views.pegar_marcas_tipo, name="pegar_marcas_tipo"),
    path('filtros/tipo/<tipo_id>/marca/<marca_id>/', views.pegar_modelos_marca, name="pegar_modelos_marca")
]
