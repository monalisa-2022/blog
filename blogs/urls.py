"""
URL configuration for blogs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
# from pages.views import home_view
from login_signup import views

urlpatterns = [
    path('sendmails/<str:uemail>', views.sendmail),
    path('checkcode/<str:uemail>', views.checkcode),
    
    path('', views.HomeView),
    path('admin/', admin.site.urls),
    path('login/', views.loginAction,name='login'),
    path('signup/', views.signupAction,name='signup'),
    path('home/', views.homeAction,name='home'),
    path('create1/', views.createAction,name='create'),
    path('home/delete/<int:id>', views.deleteAction,name='delete'),
    path('home/update/<int:id>', views.updateAction,name='update'),
    path('home/update/updaterecord/<int:id>', views.updateRecordAction,name='updaterecord'),
]