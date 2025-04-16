from django.urls import path
from . import views

urlpatterns = [
    path('', views.robot_configuration, name='robot_configuration'),
    path('control/', views.control_page, name='control'),
    path('submit/', views.submit_robot_data, name='submit_robot_data'),
    path('move/', views.handle_move, name='move'),
    path('set_robot/<int:robot_id>/', views.set_robot, name='set_robot'),
    path('set_map/<int:map_id>/', views.set_map, name='set_map'),
    path('set_speech/<int:speech_id>/', views.set_speech, name='set_speech'),
    path('play/<int:speech_id>/', views.play_speech, name='play_speech'),
    path('destination/', views.handle_guiding, name='destination'),
    path('question/', views.handle_question, name='question'),
    path('speech/', views.handle_speech, name='speech'),
    path('set_driver/', views.set_driver, name='set_driver'),
    path('restart_driver/', views.restart_driver, name='restart_driver'),
    path('stop_processes/', views.stop_processes, name='stop_processes'),
]