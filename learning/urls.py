from django.urls import path
from . import views

urlpatterns = [
    path('', views.skill_list, name='skill_list'),
    path('create/', views.skill_create, name='skill_create'),
    path('<int:pk>/', views.skill_detail, name='skill_detail'),
    path('edit/<int:pk>/', views.skill_edit, name='skill_edit'),
    path('delete/<int:pk>/', views.skill_delete, name='skill_delete'),
    path('<int:skill_pk>/topic/add/', views.topic_create, name='topic_create'),
    path('topic/edit/<int:pk>/', views.topic_edit, name='topic_edit'),
    path('topic/delete/<int:pk>/', views.topic_delete, name='topic_delete'),
    path('topic/toggle/<int:pk>/', views.topic_toggle, name='topic_toggle'),
]