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
     

def point_direction(direction="ahead", duration=3.0):
    """
    Makes Pepper point in a specified direction with its arm.
    
    Parameters:
    - direction (str): Direction to point ("ahead", "left", "right", "up", "down")
    - duration (float): How long to hold the pointing position in seconds
    
    Returns:
    - subprocess.Popen: Process object of the executed command
    """
    # Joint positions dictionary for different pointing directions
    # Format: [ShoulderPitch, ShoulderRoll, ElbowRoll, ElbowYaw, WristYaw]
    # Note: Values are in radians
    pointing_positions = {
        "ahead": {
            "right_arm": [0.2, -0.3, 0.0, 0.0, 0.0],  # Right arm extended forward
            "left_arm": [0.2, 0.3, 0.0, 0.0, 0.0]     # Left arm extended forward
        },
        "left": {
            "right_arm": [0.2, 0.3, 0.0, 1.0, 0.0],   # Right arm pointing left
            "left_arm": [0.2, 0.8, 0.0, 0.0, 0.0]     # Left arm pointing left
        },
        "right": {
            "right_arm": [0.2, -0.8, 0.0, 0.0, 0.0],  # Right arm pointing right
            "left_arm": [0.2, -0.3, 0.0, -1.0, 0.0]   # Left arm pointing right
        },
        "up": {
            "right_arm": [-1.0, -0.3, 0.0, 0.0, 0.0], # Right arm pointing up
            "left_arm": [-1.0, 0.3, 0.0, 0.0, 0.0]    # Left arm pointing up
        },
        "down": {
            "right_arm": [1.5, -0.3, 0.0, 0.0, 0.0],  # Right arm pointing down
            "left_arm": [1.5, 0.3, 0.0, 0.0, 0.0]     # Left arm pointing down
        }
    }
    
    # Check if the requested direction is valid
    if direction not in pointing_positions:
        raise ValueError(f"Direction '{direction}' not supported. Choose from: {', '.join(pointing_positions.keys())}")
    
    # We'll use the right arm for pointing by default
    arm = "right_arm"
    positions = pointing_positions[direction][arm]
    
    # Create the rostopic command to move the right arm joints
    joint_names = "RShoulderPitch,RShoulderRoll,RElbowRoll,RElbowYaw,RWristYaw"
    position_values = ",".join(map(str, positions))
    
    # Using trajectory_msgs/JointTrajectory message to control arm joints
    command = f"""rostopic pub -1 /pepper_dcm/RightArm_controller/command trajectory_msgs/JointTrajectory \
    "header:
      stamp: now
    joint_names: [{', '.join(f'"{name}"' for name in joint_names.split(','))}]
    points:
    - positions: [{position_values}]
      time_from_start:
        secs: 1"
    """

    try:
        # Execute the command in a new terminal
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Hold the position for the specified duration
        if duration > 0:
            time.sleep(duration)
            
            # Return to a neutral position after pointing
            neutral_positions = [1.0, -0.1, 0.5, 0.0, 0.0]  # Neutral position
            neutral_values = ",".join(map(str, neutral_positions))
            
            neutral_command = f"""rostopic pub -1 /pepper_dcm/RightArm_controller/command trajectory_msgs/JointTrajectory \
            "header:
              stamp: now
            joint_names: [{', '.join(f'"{name}"' for name in joint_names.split(','))}]
            points:
            - positions: [{neutral_values}]
              time_from_start:
                secs: 1"
            """

        
            
            subprocess.Popen(
                neutral_command,
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                shell=True
            )
            
        return process
        
    except Exception as e:
        print(f"Error executing pointing gesture: {e}")
        return None

def point_and_move(driver, movement_command, pointing_direction="ahead", duration=2.0):
    """
    Makes Pepper move in a direction while pointing in the specified direction,
    running each action in a separate terminal.
    
    Parameters:
    - driver (str): The driver to use ("naoqi_driver" or "pepper_dcm_bringup")
    - movement_command (str): The movement command (e.g., "avancer", "tourner à gauche")
    - pointing_direction (str): Direction to point ("ahead", "left", "right", "up", "down")
    - duration (float): How long to move and point in seconds
    
    Returns:
    - tuple: (movement_process, pointing_process)
    """
    # Start pointing gesture in its own terminal
    pointing_process = point_direction(pointing_direction, duration + 0.5)
    
    # Wait a short moment for the arm to start moving
    time.sleep(0.5)
    
    # Start the movement in its own terminal
    movement_process = move(driver, movement_command, duration)
    
    return movement_process, pointing_process

