from wikihow_research import *
from wikipedia_reseach import *
from solve_mathematics import *

def wiki_response(question, language="fr"):
    if is_math_expression(question):
        return {"text": solve_math_expression(question), "source": "Math Solver", "score": 0}
    
    response_wikipedia = rechercher_wikipedia(question, language)
    response_wikihow = rechercher_wikihow(question, language)

    if response_wikipedia["score"] > response_wikihow["score"]:
        return response_wikipedia
    else:
        return response_wikihow
    
