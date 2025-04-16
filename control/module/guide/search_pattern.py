import re

def normalize_text(text):
    """ Remplace plusieurs espaces par un seul espace """
    return re.sub(r"\s+", " ", text).strip()

