from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
import sys
import os
import json
from django.contrib.auth.decorators import login_required
from map.models import Map
from robots.models import Robot
from speech.models import Speech


# Get the base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the paths to the modules to sys.path
module_paths = [
    os.path.join(BASE_DIR, 'control', 'module', 'ia'),
    os.path.join(BASE_DIR, 'control','module', 'robotProcessManager'),
    os.path.join(BASE_DIR, 'control', 'module', 'move'),
    os.path.join(BASE_DIR, 'control', 'module', 'pepper_speach'),
    os.path.join(BASE_DIR, 'control', 'module', 'guide'),
]

for path in module_paths:
    if path not in sys.path:
        sys.path.append(path)

from best_response import wiki_response
from robotProcessManager import RobotProcessManager
from move import move
from pepper_speach import pepper_speak
from guide import guide

robot_process_manager = RobotProcessManager()
language = "fr"
priority_driver = "naoqi_driver"
matrices = [
                [
                    [0, 2, 2, 0, 1, 0],
                    [0, 0, 0, 0, 1, 0],
                    [0, 1, 0, 0, 1, 2],
                    [0, 0, 0, 0, 2, 0],
                    [2, 1, 0, 1, 1, 2]
                ]
            ]

rooms = {
        "Accueil": [0, 0, 1], 
        "Bureau des enseignants": [0, 4, 4],
        "Classe 1": [0, 0, 2],
        "Classe 2": [0, 2, 5],
        "Classe 3": [0, 4, 0],
        "Toilette": [0, 2, 5],
        "Bureau du directeur": [0, 4, 5]
    }


def robot_configuration(request):
    return render(request, 'control/form.html')


def control_page(request):
    global matrices, rooms
    if request.user.is_authenticated:
        current_map = get_object_or_404(Map, user=request.user, is_current=True)
        if not current_map:
            current_map = get_object_or_404(Map, user=request.user).first()          
        
        if current_map:
            matrices = current_map.matrices  # Use the matrices field
            rooms = current_map.rooms  # Use the rooms field
        
    return render(request, 'control/control.html',
        { 
            'matrices':json.dumps(matrices),  
            'rooms':rooms,  
            'rooms_dumps':json.dumps(rooms),  

        }
    )



@login_required
def set_robot(request, robot_id):
    global priority_driver
    user_robots = Robot.objects.filter(user=request.user)

    # Unset current flag for all maps
    user_robots.update(is_current=False)
    
    # Get the robot object or return 404 if not found
    robot = get_object_or_404(Robot, id=robot_id, user=request.user)
    
    # Set this robot as the current robot
    robot.is_current = True
    robot.save()
    
    robots = Robot.objects.filter(user=request.user)
    maps = Map.objects.filter(user=request.user)

    current_map = get_object_or_404(Map, user=request.user, is_current=True)
    if not current_map:
        current_map = get_object_or_404(Map, user=request.user).first()          
        
    if current_map:
        matrices = current_map.matrices  # Use the matrices field
        rooms = current_map.rooms  # Use the rooms field
       
    return redirect(f'/submit/?robot_ip={robot.nao_ip}&network_interface={robot.network_interface}&language={robot.language}&priority_driver={priority_driver}')
    
@login_required
def set_map(request, map_id):
    global priority_driver
    """
    # Sets the selected map as the current map for the user.
    # """
    user_maps = Map.objects.filter(user=request.user)

    # Unset current flag for all maps
    user_maps.update(is_current=False)
    
    # Set the selected map as current
    selected_map = get_object_or_404(Map, id=map_id, user=request.user)
    selected_map.is_current = True
    selected_map.save()

    robots = Robot.objects.filter(user=request.user)
    maps = Map.objects.filter(user=request.user)
    speeches = Speech.objects.filter(user=request.user)

    current_map = get_object_or_404(Map, user=request.user, is_current=True)
    if not current_map:
        current_map = get_object_or_404(Map, user=request.user).first()          
        
    if current_map:
        matrices = current_map.matrices  # Use the matrices field
        rooms = current_map.rooms  # Use the rooms field
       
    return render(request, 'control/control.html', {'robots' : robots, 'maps':maps, 'speeches': speeches, 'priority_driver': priority_driver, 'matrices':json.dumps(matrices), 'rooms':rooms, 'rooms_dumps':json.dumps(rooms),  })

    

@login_required
def set_speech(request, speech_id):
    # Get all user's speeches
    user_speeches = Speech.objects.filter(user=request.user)

    # Unset favorite flag for all speeches first
    user_speeches.update(is_favorite=False)
    
    # Get the specific speech object
    speech = get_object_or_404(Speech, id=speech_id, user=request.user)
    # Set this speech as favorite
    speech.is_favorite = True
    speech.save()
    
    robots = Robot.objects.filter(user=request.user)
    maps = Map.objects.filter(user=request.user)
    if request.user.is_authenticated:
        current_map = get_object_or_404(Map, user=request.user, is_current=True)
        if not current_map:
            current_map = get_object_or_404(Map, user=request.user).first()          
        
        if current_map:
            matrices = current_map.matrices  # Use the matrices field
            rooms = current_map.rooms  # Use the rooms field
       
    return render(request, 'control/control.html', {'robots' : robots, 'maps':maps, 'speeches': user_speeches, 'priority_driver': priority_driver, 'matrices':json.dumps(matrices), 'rooms':rooms, 'rooms_dumps':json.dumps(rooms),  })


@login_required
def play_speech(request, speech_id):
    speech = get_object_or_404(Speech, id=speech_id, user=request.user)
    pepper_speak(speech.content)
    return redirect('control')


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def submit_robot_data(request):
    global priority_driver
    try:
        if request.user.is_authenticated:
            user_robots = Robot.objects.filter(user=request.user)

            # Unset current flag for all maps
            user_robots.update(is_current=False)
    
       
        # Common processing function
        def process_data(data):
            robot_ip = data.get('robot_ip')
            network_interface = data.get('network_interface')
            language = data.get('language')
            priority_driver = data.get('priority_driver')
            
            if request.user.is_authenticated:

                # Get the robot object or return 404 if not found
                robot = get_object_or_404(Robot, nao_ip=robot_ip, user=request.user)
    
                # Set this robot as the current robot
                robot.is_current = True
                robot.save()
           
            if not all([robot_ip, network_interface, language, priority_driver]):
                raise ValueError("Missing required fields")

            # Your business logic
            robot_process_manager.start(robot_ip, network_interface)
            
            return {
                'message': 'Operation successful',
                'redirect_url': '/control/'
            }

        # Handle different methods
        if request.method == 'GET':
            result = process_data(request.GET)
            robots = Robot.objects.filter(user=request.user)
            maps = Map.objects.filter(user=request.user)
            speeches = Speech.objects.filter(user=request.user)

            if request.user.is_authenticated:
                current_map = get_object_or_404(Map, user=request.user, is_current=True)
            if not current_map:
                current_map = get_object_or_404(Map, user=request.user).first()          
        
            if current_map:
                matrices = current_map.matrices  # Use the matrices field
                rooms = current_map.rooms  # Use the rooms field
       
            return render(request, 'control/control.html', {'robots' : robots, 'maps':maps, 'speeches': speeches, 'priority_driver': priority_driver, 'matrices':json.dumps(matrices), 'rooms':rooms, 'rooms_dumps':json.dumps(rooms),  })

        elif request.method == 'POST':
            data = json.loads(request.body) if request.body else {}
            result = process_data(data)
            return JsonResponse(result)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
        
def handle_move(request):
    global robot_process_manager
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            command_move = data.get('command_move')

            if command_move:
                if priority_driver == "naoqi_driver":
                    print("test")

                    if robot_process_manager.naoqi_process is not None:

                        try:
                            move("naoqi_driver", command_move)
                            move("naoqi_driver", "stop")
                            return JsonResponse({'message': 'Le robot est en train de se déplacer via Naoqi Driver'})
                        except Exception as e:
                            print(f"Naoqi driver movement failed: {e}")
                            return JsonResponse({'message': 'Échec du déplacement avec les deux drivers'}, status=500)   
                else:
                    if robot_process_manager.pepper_process is not None:
                        try:
                            move("pepper_dcm_bringup", command_move)
                            return JsonResponse({'message': 'Le robot est en train de se déplacer via Pepper DCM'})
                        except Exception as e:
                            print(f"Pepper DCM movement failed: {e}, trying naoqi driver")
                            return JsonResponse({'message': 'Le robot est en train de se déplacer via Pepper DCM'})
                
                    else:
                        return JsonResponse({'message': 'Aucun driver robotique n\'est actif'}, status=503)
            else:
                return JsonResponse({'message': 'Aucune commande n\'a été donnée'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


def handle_guiding(request):
    global matrices, rooms, robot_process_manager, priority_driver
    current_robot = None
  
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            location = data.get('location')

            if location:
                if request.user.is_authenticated:
                    current_robot = get_object_or_404(Robot, user=request.user, is_current=True)
                
  
                if priority_driver == "naoqi_driver":
                    if robot_process_manager.naoqi_process is not None:
                        try:
                            guide("naoqi_driver", location, matrices, current_robot, rooms)

                            return JsonResponse({'message': 'Guidage en cours via Naoqi Driver'})
                        except Exception as e:
                            print(f"Naoqi driver guidance failed: {e}")
                            return JsonResponse({'message': 'Échec du guidage avec le naoqi driver'}, status=500) 
                else:
                    if robot_process_manager.pepper_process is not None:
                        try:
                            guide("pepper_dcm_bringup", location, matrices, current_robot, rooms)
                            return JsonResponse({'message': 'Guidage en cours via Pepper DCM'})
                        except Exception as e:
                            print(f"Pepper DCM guidance failed: {e}, trying naoqi driver")   
                            return JsonResponse({'message': 'Échec du guidage avec le pepper dcm bringup'}, status=50) 
                    else:
                        return JsonResponse({'message': 'Aucun driver robotique n\'est actif'}, status=503)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Cette vue ne supporte que les requêtes POST.'}, status=405)


def handle_question(request):
    global language
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question')

            if question and language:
                response = wiki_response(question, language)  # Replace with your logic
                response_text = response.get("text", "No response found.")
                pepper_speak(response_text)  # Uncomment if needed
                return JsonResponse({'message': response_text})
            else:
                return JsonResponse({'message': 'Aucune question n\'a été posée'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Cette vue ne supporte que les requêtes POST.'}, status=405)

def handle_speech(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            speech = data.get('speech')

            if speech:
                pepper_speak(speech)  # Uncomment if needed
                return JsonResponse({'message': speech})
            else:
                return JsonResponse({'message': 'Aucune phrase n\'a été fournie'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Cette vue ne supporte que les requêtes POST.'}, status=405)


@csrf_exempt
def set_driver(request):
    global priority_driver
    try:
        data = json.loads(request.body)
        priority_driver = data.get('priority_driver')
        return JsonResponse({'message': f"Driver set to {priority_driver}"})
    except:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def restart_driver(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            driver_type = data.get('driver_type', 'both')
            
            if driver_type in ['naoqi', 'both']:
                robot_process_manager.stop_naoqi_driver()
                robot_process_manager.start_naoqi_driver()
                
            if driver_type in ['pepper', 'both']:
                robot_process_manager.stop_pepper_dcm_bringup()
                robot_process_manager.start_pepper_dcm_bringup()
            
            return JsonResponse({
                'status': 'success',
                'message': f'Successfully restarted {driver_type} driver(s)'
            })
            
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'Restart failed: {str(e)}'
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)

def stop_processes(request):
    if request.method == 'POST':
        robot_process_manager.stop()
        return JsonResponse({'message': 'Tous les processus ont été arrêtés avec succès'})