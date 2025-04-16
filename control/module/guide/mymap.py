university_matrix = [
    [
        [0, 2, 2, 0, 1, 3],
        [0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 2],
        [0, 0, 0, 0, 2, 0],
        [3, 1, 0, 1, 1, 2]
    ],
    [
        [2, 0, 1, 2, 1, 3],
        [0, 2, 0, 0, 1, 2],
        [1, 0, 2, 1, 1, 0],
        [2, 2, 0, 0, 2, 1],
        [3, 1, 1, 2, 0, 2]
    ]

]

location_queries = {
    "classe 1": (0, 0, 1),
    "classe 2": (0, 0, 2),
    "classe 3": (0, 4, 0),
    "toilette": (0, 2, 5),
    "ascenseur": (0, 0, 5),
    "escalier": (0, 4, 0),
    "classe 4": (0, 3, 4),
    "bureau des enseignants": (0, 4, 5),
    "Accueil": (0, 0, 0),
    "ascenseur": (1, 0, 5),
    "escalier": (1, 4, 0),
    "bibliothèque": (1, 4, 5),
    "cafétéria": (1, 2, 3),
    "laboratoire 1": (1, 1, 2),
    "laboratoire 2": (1, 2, 0),
    "auditorium": (0, 3, 5),
}

pepper_position = [0, 3, 1]
pepper_direction = ["right"]