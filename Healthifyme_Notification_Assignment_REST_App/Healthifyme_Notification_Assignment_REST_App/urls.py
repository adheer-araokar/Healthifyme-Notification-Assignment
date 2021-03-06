"""Healthifyme_Notification_Assignment_REST_App URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Healthifyme_Notification_Assignment_REST_App import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^get_notification/(?P<num>[0-9]+)', views.NotificationView.as_view(), name='get-notification'),
    url(r'^get_query/(?P<num>[0-9]+)', views.QueryView.as_view(), name='get-query'),
    url(r'^get_user/(?P<num>[0-9]+)', views.AuthenticatedUserView.as_view(), name='get-user'),
    url(r'^put_notification/', views.NotificationView.as_view(), name='put-notification'),
    url(r'^put_query/', views.QueryView.as_view(), name='put-query'),
    url(r'^put_user/', views.AuthenticatedUserView.as_view(), name='put-user'),
]
