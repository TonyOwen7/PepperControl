import os
import json
from django.conf import settings

def get_map_file_path(user, map_id):
    """
    Returns the path of the TXT file for a given user and map ID.
    Creates the directory if it does not exist.
    """
    user_folder = os.path.join(settings.BASE_DIR, 'assets', user.username)
    os.makedirs(user_folder, exist_ok=True)  # Ensure directory exists
    return os.path.join(user_folder, f"{map_id}.txt")

def save_matrix_to_txt(user, map_id, matrix):
    """
    Saves the matrix to a TXT file, including row and column count.
    Ensures correct formatting.
    """
    file_path = get_map_file_path(user, map_id)

    if not matrix or not isinstance(matrix, list) or not all(isinstance(row, list) for row in matrix):
        raise ValueError("Invalid matrix format. Must be a list of lists.")

    rows, cols = len(matrix), len(matrix[0]) if matrix else 0

    with open(file_path, 'w') as f:
        f.write(f"{rows} {cols}\n")  # First line: row and column count
        for row in matrix:
            f.write("".join(map(str, row)) + "\n")  # Store matrix values

def load_matrix_from_txt(user, map_id):
    """
    Loads the matrix from a TXT file.
    Ensures the format is correct before returning the matrix.
    """
    file_path = get_map_file_path(user, map_id)
    if not os.path.exists(file_path):
        return None  # File does not exist

    with open(file_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        return None  # Empty file

    # Read row and column count
    try:
        rows, cols = map(int, lines[0].strip().split())
    except ValueError:
        return None  # Invalid format

    # Read and validate the matrix
    matrix = []
    for line in lines[1:]:
        row = [int(char) for char in line.strip()]
        if len(row) != cols:
            return None  # Row length does not match expected columns
        matrix.append(row)

    return matrix

def update_matrix_in_txt(user, map_id, new_matrix):
    """
    Updates an existing matrix in the TXT file, adjusting rows and columns if necessary.
    """
    if not isinstance(new_matrix, list) or not all(isinstance(row, list) for row in new_matrix):
        raise ValueError("Invalid matrix format. Must be a list of lists.")

    save_matrix_to_txt(user, map_id, new_matrix)  # Overwrite with new matrix

def rename_map_file(user, old_map_id, new_map_id):
    """
    Renames a map file if the new name is not already taken.
    Returns True if successful, False if the new name already exists.
    """
    old_file_path = get_map_file_path(user, old_map_id)
    new_file_path = get_map_file_path(user, new_map_id)

    if os.path.exists(new_file_path):
        return False  # New name already exists

    if os.path.exists(old_file_path):
        os.rename(old_file_path, new_file_path)
        return True  # Renaming successful

    return False  # Old file does not exist
