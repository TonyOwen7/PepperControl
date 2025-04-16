import os
import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Map


@login_required
def set_current_map(request, map_id):
    """
    Sets the selected map as the current map for the user.
    """
    user_maps = Map.objects.filter(user=request.user)

    # Unset current flag for all maps
    user_maps.update(is_current=False)
    
    # Set the selected map as current
    selected_map = get_object_or_404(Map, id=map_id, user=request.user)
    selected_map.is_current = True
    selected_map.save()

    return redirect('user_maps')


def read_map(file_path):
    """
    Reads a map file containing multiple 2D matrices.
    :param file_path: The file path.
    :return: A dictionary containing num_matrices, rows, cols, and matrices.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.read().strip().split('\n')
            
            # Read the first line: num_matrices, rows, cols
            num_matrices, rows, cols = map(int, lines[0].split())
            
            matrices = []
            current_line = 1
            
            for _ in range(num_matrices):
                # Read the matrix
                matrix = []
                for _ in range(rows):
                    row = list(map(int, lines[current_line].split()))
                    if len(row) != cols:
                        raise ValueError("Matrix dimensions do not match the specified size.")
                    matrix.append(row)
                    current_line += 1
                
                matrices.append(matrix)
                
                # Skip the blank line between matrices
                if current_line < len(lines) and lines[current_line].strip() == '':
                    current_line += 1
            
            return {
                "num_matrices": num_matrices,
                "rows": rows,
                "cols": cols,
                "matrices": matrices,
            }
    except Exception as e:
        print(f"Error: {e}")
        return None
def write_matrix_to_file(file_path, matrices, rows, cols):
    """
    Writes multiple 2D matrices to a file.
    :param file_path: The file path.
    :param matrices: A list of 2D matrices.
    :param rows: Number of rows in each matrix.
    :param cols: Number of columns in each matrix.
    """
    try:
        num_matrices = len(matrices)
        content = f"{num_matrices} {rows} {cols}\n"
        
        for matrix in matrices:
            content += '\n'.join(' '.join(map(str, row)) for row in matrix) + '\n\n'
        
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"File successfully created at: {file_path}")
    except Exception as e:
        print(f"Error while creating the file: {e}")

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
from .models import Map
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
from .models import Map

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
from .models import Map
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
from .models import Map

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from django.shortcuts import redirect
@login_required
def save_map(request):
    print("save")
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method. POST required.'}, status=405)

    try:
        # Parse the request body (JSON data)
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            matrices = data.get('matrices')
            rows = data.get('rows')
            cols = data.get('cols')
            rooms = data.get('rooms')  # Get the rooms dictionary
            map_id = data.get('id')
            map_name = data.get('name')
        else:
            # Parse form data
            data = json.loads(request.body)
            matrices = data.get('matrices')
            rows = data.get('rows')
            cols = data.get('cols')
            rooms = data.get('rooms')  # Get the rooms dictionary
            map_id = data.get('id')
            map_name = data.get('name')
        print("[save] rooms: ", rooms)
        # Validate required fields
        if not matrices or not map_id or not map_name:
            return JsonResponse({'error': 'Matrices data, map ID, or map name is missing.'}, status=400)

        # Fetch the existing map
        map_instance = get_object_or_404(Map, id=map_id, user=request.user)

        # Update the matrices, rows, cols, rooms, and map name
        map_instance.matrices = matrices
        map_instance.rows = rows
        map_instance.cols = cols
        map_instance.rooms = rooms
        map_instance.name = map_name
        map_instance.save()

        # Save the matrix to a text file
        user_folder = os.path.join(settings.BASE_DIR, 'assets', request.user.username)
        os.makedirs(user_folder, exist_ok=True)
        file_path = os.path.join(user_folder, f"{map_instance.name}.txt")
        write_matrix_to_file(file_path, matrices, rows, cols)

        # Redirect to the user_maps page
        return redirect('user_maps')

    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'JSON parsing failed: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Map
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import json
from .models import Map

import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
import os
from .models import Map

@login_required
def edit_map(request, map_name=None, map_id=None):
    """
    Renders the map editor for creating or editing a map.
    If map_id is provided, loads the existing map; otherwise, creates a new one.
    """
    if map_id:
        # Load existing map
        map_instance = get_object_or_404(Map, id=map_id, user=request.user)

    else:
        # Create a new map
        default_name = f"Map {Map.objects.filter(user=request.user).count() + 1}"  # Generate a default name
        matrices = [[[0 for _ in range(4)] for _ in range(4)]]  # Default 4x4 empty matrix
        rooms = {}
        rows, cols = 4, 4

        # Create the new map instance
        map_instance = Map.objects.create(
            user=request.user,
            name=default_name,
            matrices=matrices,
            rows=rows,
            cols=cols,
            rooms=rooms,
            is_default=False,
            is_current=False
        )

        # Ensure the assets/username directory exists
        user_folder = os.path.join(settings.BASE_DIR, 'assets', request.user.username)
        os.makedirs(user_folder, exist_ok=True)

        # Save the matrix to a text file
        file_path = os.path.join(user_folder, f"{map_instance.name}.txt")
        write_matrix_to_file(file_path, matrices, rows, cols)

    # Serialize matrices to JSON
    matrices_json = json.dumps(map_instance.matrices)
    rooms_json =  json.dumps(map_instance.rooms)

    return render(request, 'map/map_editor.html', {
        'map': map_instance,
        'matrices_json': matrices_json,
        'rooms' : rooms_json,
    })
    
@login_required
@csrf_exempt
def save_map(request):
    if request.method != "POST":
        return JsonResponse({'error': 'Invalid request method. POST required.'}, status=405)

    try:
        # Parse the request body (JSON data)
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            matrices = data.get('matrices')
            rows = data.get('rows')
            cols = data.get('cols')
            rooms = data.get('rooms')  # Get the rooms dictionary
            map_id = data.get('id')
            map_name = data.get('name')
        else:
            # Parse form data
            matrices = json.loads(request.POST.get('matrices', '[]'))
            rows = int(request.POST.get('rows', 4))
            cols = int(request.POST.get('cols', 4))
            rooms = json.loads(request.POST.get('rooms'))  # Get the rooms dictionary
            map_id = request.POST.get('map_id')
            map_name = request.POST.get('name')

        # Validate required fields
        if not matrices or not map_id or not map_name:
            return JsonResponse({'error': 'Matrices data, map ID, or map name is missing.'}, status=400)

        # Fetch the existing map
        map_instance = get_object_or_404(Map, id=map_id, user=request.user)

        # Update the matrices, rows, cols, rooms, and map name
        map_instance.matrices = matrices
        map_instance.rows = rows
        map_instance.cols = cols
        map_instance.rooms = rooms
        map_instance.name = map_name
        map_instance.save()

        # Save the matrix to a text file
        user_folder = os.path.join(settings.BASE_DIR, 'assets', request.user.username)
        os.makedirs(user_folder, exist_ok=True)
        file_path = os.path.join(user_folder, f"{map_instance.name}.txt")
        write_matrix_to_file(file_path, matrices, rows, cols)

        # Redirect to the user_maps page
        return redirect('user_maps')

    except json.JSONDecodeError as e:
        return JsonResponse({'error': f'JSON parsing failed: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)
@login_required
def delete_map(request, map_id):
    """
    Deletes a map and its associated TXT file.

    """
    map_instance = get_object_or_404(Map, id=map_id, user=request.user)

    file_path = f"assets/{request.user.username}/{map_instance.name}.txt"

    if os.path.exists(file_path):
        os.remove(file_path)  # Delete the TXT file

    map_instance.delete()  # Delete from database

    return redirect('user_maps')


@login_required
def user_maps(request):
    """
    Displays all maps associated with the logged-in user.
    """
    maps = Map.objects.filter(user=request.user)
    current_map = None
    if not maps.exists():
        current_map = maps.filter(is_favorite=True)
        if not current_map:
            current_map = maps.first() 
            current_map.is_current = True   
            current_map.save()    
    return render(request, 'map/user_maps.html', {'maps': maps})


@csrf_exempt
@login_required
def get_map(request, map_id):
    """
    API to fetch the matrix data for a specific map.
    """
    map_instance = get_object_or_404(Map, id=map_id, user=request.user)
    return JsonResponse({'matrix': map_instance.matrix})
