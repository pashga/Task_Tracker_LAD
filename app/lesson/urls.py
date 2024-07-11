from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='projects_list'),
    path('registration/', views.registration, name='registration'),
    path('project_form/', views.project_create, name='project_create'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('project/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('project/<int:pk>/add_members/', views.project_add_members, name='project_add_members'),
    path('project/<int:project_pk>/delete_member/<int:user_pk>', views.project_delete_members, name='project_delete_member'),
    path('project/<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('project/<int:project_pk>/task_create/', views.task_create, name='task_create'),
    path('task/<int:pk>/', views.task_detail, name='task_detail'),
    path('task/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task_delete'),
]
