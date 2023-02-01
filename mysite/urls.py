from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
		path('', views.home, name= 'home'),
    path('admin/', admin.site.urls),
		path('get_weather/', views.get_weather, name="get_weather")
]