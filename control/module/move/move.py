#!/usr/bin/env python
# movement_controller.py

import rospy
from geometry_msgs.msg import Twist

import sys
import time
from mymap import  pepper_position, pepper_direction
import subprocess

def move2(driver, command_name, duration=0.5):

    naoqi_commands = {
        "stop": {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/cmd_vel', 'direction': 'stop'},
        "avancer": {'linear': [1.0, 0.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/cmd_vel', 'direction': 'down'},
        "reculer": {'linear': [-1.0, 0.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/cmd_vel', 'direction': 'up'},
        "aller à gauche": {'linear': [0.0, 1.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/cmd_vel', 'direction': 'left'},
        "aller à droite": {'linear': [0.0, -1.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/cmd_vel', 'direction': 'right'},
        "avancer vers gauche": {'linear': [1.0, 1.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/cmd_vel', 'direction': 'down_left'},
        "avancer vers droite": {'linear': [1.0, -1.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/cmd_vel', 'direction': 'down_right'},
        "reculer vers gauche": {'linear': [-1.0, 1.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/cmd_vel', 'direction': 'up_left'},
        "reculer vers droite": {'linear': [-1.0, -1.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/cmd_vel', 'direction': 'up_right'},
        "tourner à gauche": {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, 0.7854], 'topic': '/cmd_vel', 'direction': 'left'},
        "tourner à droite": {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, -0.7854], 'topic': '/cmd_vel', 'direction': 'right'},
        "demi-tour gauche": {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, 1.5706], 'topic': '/cmd_vel', 'direction': 'left'},
        "demi-tour droit": {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, -1.5706], 'topic': '/cmd_vel', 'direction': 'right'},
    }

    dcm_commands = {
        "stop": {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'stop'},
        "avancer": {'linear': [0.5, 0.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'down'},
        "reculer": {'linear': [-0.5, 0.0, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'up'},
        "aller à gauche": {'linear': [0.0, 0.5, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'left'},
        "aller à droite": {'linear': [0.0, -0.5, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'right'},
        "avancer vers gauche": {'linear': [0.5, 0.5, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'down_left'},
        "avancer vers droite": {'linear': [0.5, -0.5, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'down_right'},
        "reculer vers gauche": {'linear': [-0.5, 0.5, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'up_left'},
        "reculer vers droite" : {'linear': [-0.5, -0.5, 0.0], 'angular': [0.0, 0.0, 0.0], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'up_right'},
        'tourner à gauche': {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, 0.7854], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'left'},
        'tourner à droite': {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, -0.7854], 'topic': '/pepper_dcm/cmd_moveto', 'direction': 'right'},
        "demi-tour gauche": {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, 1.5706], 'topic': '/cmd_vel', 'direction': 'left'},
        "demi-tour droit": {'linear': [0.0, 0.0, 0.0], 'angular': [0.0, 0.0, -1.5706], 'topic': '/cmd_vel', 'direction': 'right'},
    }

    command = naoqi_commands if driver == 'naoqi_driver' else dcm_commands

    if command_name not in command:
        rospy.logerr(f"Commande {command_name} non trouvée pour le driver {driver}")
        return pepper_position

    rospy.init_node('pepper_movement', anonymous=True, disable_signals=True)

    # Publisher for movement commands
    pub_move = rospy.Publisher(command[command_name]['topic'], Twist, queue_size=10)
    
    move_cmd = Twist()
    move_cmd.linear.x = command[command_name]['linear'][0]
    move_cmd.linear.y = command[command_name]['linear'][1]
    move_cmd.linear.z = command[command_name]['linear'][2]
    move_cmd.angular.x = command[command_name]['angular'][0]
    move_cmd.angular.y = command[command_name]['angular'][1]
    move_cmd.angular.z = command[command_name]['angular'][2]
    
    rate = rospy.Rate(10)
    time_elapsed = 0
    if driver == "naoqi_driver":
        duration = duration * 2
    while time_elapsed < duration:
        pub_move.publish(move_cmd)
        time_elapsed += 0.1
        rate.sleep()

    # Stop movement
    move_cmd.linear.x = 0
    move_cmd.linear.y = 0
    move_cmd.linear.z = 0
    move_cmd.angular.x = 0
    move_cmd.angular.y = 0
    move_cmd.angular.z = 0

    time_elapsed = 0

    while time_elapsed < 0.5:
        pub_move.publish(move_cmd)
        time_elapsed += 0.1
        rate.sleep()
    

def move(driver, command_name, duration=0.5):
    """Envoie une commande de mouvement à Pepper via rostopic pub"""
    
    # Dictionnaire complet des commandes de mouvement
    movement_commands = {
        "naoqi_driver": {
            "stop": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "avancer": "'{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "reculer": "'{linear: {x: -0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "aller à gauche": "'{linear: {x: 0.0, y: 0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "aller à droite": "'{linear: {x: 0.0, y: -0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "avancer vers gauche": "'{linear: {x: 0.5, y: 0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "avancer vers droite": "'{linear: {x: 0.5, y: -0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "reculer vers gauche": "'{linear: {x: -0.5, y: 0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "reculer vers droite": "'{linear: {x: -0.5, y: -0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "tourner à gauche": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.7854}}'",
            "tourner à droite": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: -0.7854}}'",
            "demi-tour gauche": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.5706}}'",
            "demi-tour droit": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: -1.5706}}'"
        },
        "pepper_dcm_bringup": {
            "stop": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "avancer": "'{linear: {x: 0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "reculer": "'{linear: {x: -0.5, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "aller à gauche": "'{linear: {x: 0.0, y: 0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "aller à droite": "'{linear: {x: 0.0, y: -0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "avancer vers gauche": "'{linear: {x: 0.5, y: 0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "avancer vers droite": "'{linear: {x: 0.5, y: -0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "reculer vers gauche": "'{linear: {x: -0.5, y: 0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "reculer vers droite": "'{linear: {x: -0.5, y: -0.5, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}'",
            "tourner à gauche": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.7854}}'",
            "tourner à droite": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: -0.7854}}'",
            "demi-tour gauche": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.5706}}'",
            "demi-tour droit": "'{linear: {x: 0.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: -1.5706}}'"
        }
    }

    # Sélection du topic selon le driver
    topic = "/cmd_vel" if driver == "naoqi_driver" else "/pepper_dcm/cmd_moveto"
    
    if driver not in movement_commands or command_name not in movement_commands[driver]:
        raise ValueError(f"Commande {command_name} non valide pour le driver {driver}")

    # Construction de la commande rostopic
    command = (f"rostopic pub -1 {topic} geometry_msgs/Twist "
              f"{movement_commands[driver][command_name]}")

    try:
        # Exécution de la commande
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Attendre la fin du mouvement si une durée est spécifiée
        if duration > 0:
            time.sleep(duration)
            stop_command = (f"rostopic pub -1 {topic} geometry_msgs/Twist "
                          f"{movement_commands[driver]['stop']}")
            subprocess.run(stop_command, shell=True)
            
        return process
        
    except Exception as e:
        print(f"Erreur lors de l'exécution: {e}")
     