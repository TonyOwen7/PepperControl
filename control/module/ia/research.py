import sys
import os

module_path = os.path.join(os.path.dirname(__file__), '../module')
sys.path.append(module_path)

import requests
from bs4 import BeautifulSoup
import re
from collections import Counter



def extract_keywords(text):
    """Extract keywords from text."""
    return set(re.findall(r'\w+', text.lower()))

def count_keyword_occurrences(text, keywords):
    """Count occurrences of each keyword in the given text."""
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(words)
    return sum(word_counts[keyword] for keyword in keywords)

def find_most_relevant_paragraphs(text, question_keywords, max_paragraphs=3):
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    scored_paragraphs = []

    for paragraph in paragraphs:
        # Calculate relevance based on occurrences of keywords in paragraph
        score = count_keyword_occurrences(paragraph, question_keywords)
        if score > 0:
            scored_paragraphs.append((score, paragraph))

    # Sort paragraphs by score in descending order and get top paragraphs
    scored_paragraphs.sort(reverse=True, key=lambda x: x[0])
    top_paragraphs = [p[1] for p in scored_paragraphs[:max_paragraphs]]
    return " ".join(top_paragraphs)

def best_text(myList):
    the_best_text = myList[0]

    for text in myList:
        if text["score"] > the_best_text["score"]:
            the_best_text = text
    return the_best_text