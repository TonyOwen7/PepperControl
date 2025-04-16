from research import *

def rechercher_wikipedia(question, language="fr"):
    url = f"https://{language}.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": question,
        "format": "json",
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        keywords = extract_keywords(question)

        for result in data["query"]["search"]:
            page_id = result["pageid"]
            content_url = f"https://{language}.wikipedia.org/w/api.php?action=query&prop=extracts&pageids={page_id}&exintro=&format=json"
            content_response = requests.get(content_url)
            content_response.raise_for_status()
            content_data = content_response.json()
            page_content = content_data["query"]["pages"][str(page_id)]["extract"]
            page_text = BeautifulSoup(page_content, "html.parser").get_text().strip().lower()

            relevant_text = find_most_relevant_paragraphs(page_text, keywords)
            return {"text": relevant_text, "source": "Wikipedia", "score": count_keyword_occurrences(relevant_text, keywords)}

        return {"text": "Aucun résultat trouvé sur Wikipedia.", "source": "Wikipedia", "score": 0}

    except Exception as e:
        return {"text": f"Erreur lors de la récupération d'informations sur Wikipedia : {e}", "source": "Wikipedia", "score": 0}
