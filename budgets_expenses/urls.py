"""budgets_expenses URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# Importar vistas (controlador) de la app mainapp.
from mainapp import views as mainapp_views

urlpatterns = [

    path('admin/', admin.site.urls),

    # url creadas.

    path('',mainapp_views.initial,name='url_initial'),
    path('initial/',mainapp_views.initial,name='url_initial'),

    path('login/',mainapp_views.login,name='url_login'),
    path('register/',mainapp_views.register,name='url_register'),

    path('presupuestos_gastos/',mainapp_views.presupuestosGastos,name='url_presupuestos_gastos'),
    path('establecimientos/',mainapp_views.establecimientos,name='url_establecimientos'),
    path('objetos_gasto/',mainapp_views.objetosGasto,name='url_objetos_gasto'),

    path('ingresar_establecimiento/',mainapp_views.ingresarEstablecimiento,name='url_ingresar_establecimiento'),
    path('editar_establecimiento/<str:establecimiento_id>/',mainapp_views.editarEstablecimiento,name='url_editar_establecimiento'),
    path('eliminar_establecimiento/<str:establecimiento_id>/',mainapp_views.eliminarEstablecimiento,name='url_eliminar_establecimiento'),

    path('ingresar_objeto_gasto/',mainapp_views.ingresarObjetoGasto,name='url_ingresar_objeto_gasto'),
    path('editar_objeto_gasto/<str:objeto_id>/',mainapp_views.editarObjetoGasto,name='url_editar_objeto_gasto'),
    path('eliminar_objeto_gasto/<str:objeto_id>/',mainapp_views.eliminarObjetoGasto,name='url_eliminar_objeto_gasto'),

    path('mostrar_informes/',mainapp_views.mostrarInformes,name='url_mostrar_informes'),
    path('ingresar_pyg/',mainapp_views.ingresarPyG,name='url_ingresar_pyg'),

]