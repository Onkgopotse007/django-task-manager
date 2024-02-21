from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('task/create/', views.task_create, name='task_create'),
    re_path(r'^tasks/(?P<task_id>\d+)/edit/$', views.task_edit, name='task_edit'),
    re_path(r'^tasks/(?P<task_id>\d+)/delete/$', views.task_delete, name='task_delete'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    re_path(r'^tasklist/$', views.task_listboard, name='task_listboard'),
]
