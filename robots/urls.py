from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_robots, name='user_robots'),
    path('set_current_robot/<int:robot_id>/<str:page>', views.set_current_robot, name='set_current_robot'),
    path('create/', views.create_robot, name='create_robot'),
    path('control/<int:robot_id>/', views.control_robot, name='control_robot'),
    path('robots/delete/<int:robot_id>/', views.delete_robot, name='delete_robot'),
    path('edit_robot/<int:robot_id>/', views.edit_robot, name='edit_robot'),
]