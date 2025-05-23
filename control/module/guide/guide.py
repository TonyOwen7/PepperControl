import sys
import os

move_path = os.path.join(os.path.dirname(__file__), '../move')
mymap_path = os.path.join(os.path.dirname(__file__), '../mymap')
shortest_path_path = os.path.join(os.path.dirname(__file__), '../shortest_path')
search_pattern_path = os.path.join(os.path.dirname(__file__), '../search_pattern')
pepper_speach_path =   os.path.join(os.path.dirname(__file__), '../pepper_speach'),

sys.path.append(move_path)
sys.path.append(mymap_path)
sys.path.append(shortest_path_path)
sys.path.append(search_pattern_path)
sys.path.append(pepper_speach_path)

from move import *
from mymap import university_matrix, location_queries, pepper_direction, pepper_position
from shortest_path import *
from search_pattern import *
from collections import deque
from pepper_speach import pepper_speak

def clearup_sequence_of_moves(commands):
    if not commands:
        return deque()  

    file_of_commandes = deque()
    file_of_commandes.append([commands[0], 0.5])  

    for command in commands[1:]:
        last_command, last_time = file_of_commandes[-1]  
        if command == last_command:
            file_of_commandes[-1][1] += 0.5
        else:
            file_of_commandes.append([command, 0.5])

    return file_of_commandes

def upgrade_position_and_direction(path):
    global pepper_position, pepper_direction
    commands = []
    for i in range(len(path)):
        if i == 0 or path[i][0] == path[i - 1][0]:
            if pepper_direction[0] == "up":
                if path[i][1] < pepper_position[1]:
                    commands.append("avancer")
                if path[i][1] > pepper_position[1]:
                    pepper_direction[0] = "bottom"
                    commands.append("demi-tour gauche")
                    commands.append("avancer")
                if path[i][2] < pepper_position[2]:
                    pepper_direction[0] = "left"
                    commands.append("tourner à gauche")
                    commands.append("avancer")
                if path[i][2] > pepper_position[2]:
                    pepper_direction[0] = "right"
                    commands.append("tourner à droite")
                    commands.append("avancer")

            elif pepper_direction[0] == "bottom":
                if path[i][1] < pepper_position[1]:
                    pepper_direction[0] = "up"
                    commands.append("demi-tour gauche")
                    commands.append("avancer")
                if path[i][1] > pepper_position[1]:
                    commands.append("avancer")
                if path[i][2] < pepper_position[2]:
                    pepper_direction[0] = "left"
                    commands.append("tourner à droite")
                    commands.append("avancer")
                if path[i][2] > pepper_position[2]:
                    pepper_direction[0] = "right"
                    commands.append("tourner à gauche")
                    commands.append("avancer")

            elif pepper_direction[0] == "left":
                if path[i][1] < pepper_position[1]:
                    pepper_direction[0] = "up"
                    commands.append("tourner à droite")
                    commands.append("avancer")
                if path[i][1] > pepper_position[1]:
                    pepper_direction[0] = "bottom"
                    commands.append("tourner à gauche")
                    commands.append("avancer")
                if path[i][2] < pepper_position[2]:
                    commands.append("avancer")
                if path[i][2] > pepper_position[2]:
                    pepper_direction[0] = "right"
                    commands.append("demi-tour gauche")
                    commands.append("avancer")

            elif pepper_direction[0] == "right":
                if path[i][1] < pepper_position[1]:
                    pepper_direction[0] = "up"
                    commands.append("tourner à gauche")
                    commands.append("avancer")
                if path[i][1] > pepper_position[1]:
                    pepper_direction[0] = "bottom"
                    commands.append("tourner à droite")
                    commands.append("avancer")
                if path[i][2] < pepper_position[2]:
                    pepper_direction[0] = "left"
                    commands.append("demi-tour gauche")
                    commands.append("avancer")
                if path[i][2] > pepper_position[2]:
                    commands.append("avancer")

            pepper_position[1] = path[i][1]
            pepper_position[2] = path[i][2]
        else:
            commands.append("monter")
            pepper_position[0] = path[i][0]

                                                  
    return commands
def guide_aux(path, driver, language="fr"):
    """
    Guides the user along a path using movement commands.
    
    Parameters:
    - path (list): Path sequence to follow.
    - driver (str): The control system (e.g., "naoqi_driver").
    - language (str): Language for verbal instructions ("fr" or "en").
    """
    commands = clearup_sequence_of_moves(upgrade_position_and_direction(path))

    translations = {
        "fr": {
            "follow_me": "Allons-y",
            "cannot_climb": "Là, je ne peux plus monter, je vais vous guider vers votre destination. Maintenant, il faudra prendre l'ascenseur.",
            "take_elevator": "Prendre l'ascenseur"
        },
        "en": {
            "follow_me": "Let's go",
            "cannot_climb": "At this point, I can't go upstairs, so I'll guide you to your destination. Now, you need to take the elevator.",
            "take_elevator": "Take the elevator."
        }
    }
    
    lang_texts = translations.get(language, translations["fr"])  # Defaults to French if unsupported language

    go_up_to_the_next_floor = False
    i = 0

    # Start movement process
    pepper_speak(lang_texts["follow_me"])
    point_and_move(driver, commands[0][0], commands[0][1])
    i += 1

    while i < len(commands) and not go_up_to_the_next_floor:
        if commands[i][0] == "monter":
            go_up_to_the_next_floor = True
        move(driver, commands[i][0], commands[i][1])
        if driver == "naoqi_driver":
            move(driver, "stop")
        i += 1

    if go_up_to_the_next_floor:
        pepper_speak(lang_texts["cannot_climb"])

        while i < len(commands):
            if commands[i][0] == "monter":
                pepper_speak(lang_texts["take_elevator"])
            else:
                pepper_speak(commands[i][0])
            i += 1

    print("Guide complete.")

            
import re

def guide(driver, chosen_location, myMap=None, robot=None, myLocationQueries=None, language="fr"):
    global university_matrix, location_queries, pepper_position, pepper_direction
    
    # Translation dictionary
    translations = {
        "fr": {
            "follow_me": "Suivez-moi, je vais vous mener vers ",
            "destination_unreachable": "Désolé, je ne peux pas atteindre cette destination.",
            "guidance_intro": "Pour aller à ",
            "next_steps": "il faut suivre le guidage suivant, voici ce que vous allez faire:",
            "cannot_climb": "Je ne pourrai pas monter, je vais vous guider vers votre destination. Maintenant, il faudra prendre l'ascenseur",
            "take_elevator": "Prendre l'ascenseur"
        },
        "en": {
            "follow_me": "Follow me, I will lead you to ",
            "destination_unreachable": "Sorry, I can't reach this destination.",
            "guidance_intro": "To get to ",
            "next_steps": "you need to follow this guidance, here is what you will do:",
            "cannot_climb": "I cannot go upstairs, I will guide you to your destination. Now, you need to take the elevator",
            "take_elevator": "Take the elevator"
        }
    }

    # Get translations based on the language choice
    lang_texts = translations.get(language, translations["fr"])  # Defaults to French if unsupported language
    
    # Update Pepper position if robot is provided
    if robot:
        pepper_position = [robot.floor, robot.row, robot.column] 
        pepper_direction = [robot.direction] 

    location_db = location_queries if robot else myLocationQueries
    matrix_db = university_matrix if robot else myMap

    for location, (floor, row, col) in location_db.items():
        if re.search(re.sub(r"\s+", r"\\s+", location), chosen_location, re.IGNORECASE):
            print(f"Location found: {location}, at floor {floor}, row {row}, column {col}")
            path = bfs(matrix_db, tuple(pepper_position), (floor, row, col))

            if path:
                pepper_speak(lang_texts["follow_me"] + location)
                print("Path:", path)

                go_up_to_the_next_floor = False
                i = 0

                pepper_speak(lang_texts["guidance_intro"] + location + " " + lang_texts["next_steps"])
                while i < len(commands) and not go_up_to_the_next_floor:
                    if commands[i][0] == "monter":
                        go_up_to_the_next_floor = True
                        continue
                    pepper_speak(commands[i][0])
                    i += 1

                if go_up_to_the_next_floor:
                    pepper_speak(lang_texts["cannot_climb"])

                    while i < len(commands):
                        if commands[i][0] == "monter":
                            pepper_speak(lang_texts["take_elevator"])
                        else:
                            pepper_speak(commands[i][0])
                        i += 1

                guide_aux(path, driver)  
            else:
                pepper_speak(lang_texts["destination_unreachable"])
                print(lang_texts["destination_unreachable"])
            break
    else:
        for location in myLocationQueries.keys():
            location_regex = re.sub(r"\s+", r"\\s+", location)

            if re.search(location_regex, chosen_location, re.IGNORECASE):
                floor, row, col = myLocationQueries[location]
                print(f"Location found: {location}, at floor {floor} row {row}, column {col}")
                path = bfs(myMap, tuple(pepper_position), (floor, row, col))
                
                if path is not None:

                    pepper_speak(lang_texts["follow_me"] + location)
                print("Path:", path)

                go_up_to_the_next_floor = False
                i = 0

                pepper_speak(lang_texts["guidance_intro"] + location + " " + lang_texts["next_steps"])
                while i < len(commands) and not go_up_to_the_next_floor:
                    if commands[i][0] == "monter":
                        go_up_to_the_next_floor = True
                        continue
                    pepper_speak(commands[i][0])
                    i += 1

                if go_up_to_the_next_floor:
                    pepper_speak(lang_texts["cannot_climb"])

                    while i < len(commands):
                        if commands[i][0] == "monter":
                            pepper_speak(lang_texts["take_elevator"])
                        else:
                            pepper_speak(commands[i][0])
                        i += 1

                guide_aux(path, driver)  
            else:
                pepper_speak(lang_texts["destination_unreachable"])
                print(lang_texts["destination_unreachable"])
            break