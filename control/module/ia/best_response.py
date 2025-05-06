from wikihow_research import *
from wikipedia_reseach import *
from solve_mathematics import *


def clean_text(text):
    """
    Cleans up the input text by:
    - Removing references like [16], [13], etc.
    - Fixing capitalization errors at the beginning of sentences.
    - Trimming extra spaces.
    
    Args:
        text (str): Raw input text.
        
    Returns:
        str: Cleaned-up text.
    """
    # Remove reference numbers in brackets
    cleaned_text = re.sub(r'\[\d+\]', '', text)

    # Ensure first letter in sentences is capitalized
    sentences = cleaned_text.split('. ')
    cleaned_sentences = [sentence.capitalize() for sentence in sentences]
    
    # Join sentences back into a paragraph
    cleaned_text = '. '.join(cleaned_sentences)

    return cleaned_text.strip()

    raw_text = """tudy a few days before the test. Don't cram for a test. As soon as the date is announced, start preparing. Look over your notes and textbook to review the material each day for a few days before the test. This way, you avoid anxiety the night before the test by trying to learn everything in a few hours.[16] Write down all the formulas you need at the start of the test. Most math tests involve remembering numerous formulas to solve different problems. Even if you studied and know them well, you could forget some if you get nervous during the test. Prevent this by doing a “brain dump” and writing down all the necessary formulas at the beginning of the test. Then refer back to this list if you forget any formulas. Pay attention during class. The work of preparing for a test begins long before the actual test. If you're attentive during class, you'll know the material much better for test day. Always get to class on time, take out your pen and notebook, and be ready to work.[13]"""

    cleaned_text = clean_text(raw_text)


def wiki_response(question, language="fr"):
    if is_math_expression(question):
        return {"text": solve_math_expression(question), "source": "Math Solver", "score": 0}
    
    response_wikipedia = rechercher_wikipedia(question, language)
    response_wikihow = rechercher_wikihow(question, language)

    if response_wikipedia["score"] > response_wikihow["score"]:
        response_wikipedia["text"] = clean_text(response_wikipedia["text"])
        return response_wikipedia
    else:
        response_wikihow["text"] = clean_text(response_wikihow["text"])
        return response_wikihow
    
