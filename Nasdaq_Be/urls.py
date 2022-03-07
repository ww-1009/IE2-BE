"""Nasdaq_Be URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from apps.nasdaq import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('nasdaq/index_7/',views.query_index_7), # 获取index_3的信息接口
    path('nasdaq/entitydata/',views.getentityData),
    path('nasdaq/porpertydata/',views.getporpertyData),
    path('nasdaq/newstop/',views.getnewstop)
]