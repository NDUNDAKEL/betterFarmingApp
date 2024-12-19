"""
URL configuration for betterFarming project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from betterFarming import settings
from betterFarmingApp import views
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),   
    path('', views.loginFunction, name='loginPage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),

    path('blog/', views.blog, name='blog'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('adminLogin/', views.adminLogin, name='adminLogin'),
    path('addPlants/', views.add_plant, name='addPlants'),
    path('plant_list/', views.plant_list, name='plant_list'),
    path('logout/', views.logout_view, name='logout'),
    path('delete_plant/<int:plant_id>/', views.delete_plant, name='delete_plant'),
    path('edit_plant/<int:plant_id>/', views.edit_plant, name='edit_plant'),
  


    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
