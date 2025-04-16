import sys
import os

module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'module'))
move_path = os.path.join(os.path.dirname(__file__), 'move')
guide_path = os.path.join(os.path.dirname(__file__), 'guide')
mymap_path = os.path.join(os.path.dirname(__file__), 'mymap')
pepper_speak_path = os.path.join(os.path.dirname(__file__), 'pepper_speach')
best_response_path = os.path.join(os.path.dirname(__file__), 'ia')
robot_process_manager_path = os.path.join(os.path.dirname(__file__), 'robotProcessManager')
pepper_listen_path = os.path.join(os.path.dirname(__file__), 'pepper_listen')

sys.path.append(module_path)
sys.path.append(move_path)
sys.path.append(guide_path)
sys.path.append(mymap_path)
sys.path.append(pepper_speak_path)
sys.path.append(best_response_path)
sys.path.append(robot_process_manager_path)
sys.path.append(pepper_listen_path)

from flask import Flask, render_template, request, jsonify, redirect, url_for
from best_response import wiki_response
from robotProcessManager import RobotProcessManager
from move import move
from pepper_speach import pepper_speak
from guide import guide
from pepper_listen import pepper_listen, process_input


app = Flask(__name__, template_folder="templates", static_folder="static")
wiki_mode_enabled = False

robot_process_manager = RobotProcessManager()


@app.route('/')
def robot_configuration():
    return render_template('form.html')

@app.route('/control')
def control_page():
    return render_template('control.html')

@app.route('/submit', methods=['POST'])
def submit_robot_data():
    global language
    data = request.json
    robot_ip = data['robot_ip']
    network_interface = data['network_interface']
    language = data['language']
    
    robot_process_manager.start(robot_ip, network_interface)

    return jsonify({
        'redirect_url': url_for('control_page', 
                                language=language,
                                )
    })

@app.route('/move', methods=['POST'])
def handle_move():
    data = request.get_json()
    command_move = data['command_move']

    if command_move:
        move("pepper_dcm_bringup", command_move)
        return jsonify({'response': 'Le robot est en train de se déplacer'})
    else:
        return jsonify({'response': 'Aucune commande n\'a été donnée'})


@app.route('/destination', methods=['POST'])
def handle_guiding():
    data = request.get_json()
    location = data['destination']

    if location:
        guide("pepper_dcm_bringup", location)
        return jsonify({'response': 'Le robot est en train de se déplacer vers la destination'})
    else:
        return jsonify({'response': 'Aucune commande n\'a été donnée'})

@app.route('/question', methods=['POST'])
def handle_question():
    data = request.get_json()
    question = data['question']
    language = data['language']
    
    if question:
        response = wiki_response(question, language)
        response = response["text"]
        pepper_speak(response)
        return jsonify({'response': response})
    else:
        return jsonify({'response': 'Aucune question n\'a été posée'})

@app.route('/speech', methods=['POST'])
def handle_speech():
    data = request.get_json()
    speech = data['speech']
    
    if question:
        pepper_speak(speech)
        return jsonify({'response': speech})    
    else:
        return jsonify({'response': 'Aucune question n\'a été posée'})
        

@app.route('/stop_processes', methods=['POST'])
def stop_processes():
    robot_process_manager.stop()
    return jsonify({'message': 'Tous les processus ont été arrêtés avec succès'})

language = "fr"

if __name__ == '__main__':
    app.run(debug=True)

