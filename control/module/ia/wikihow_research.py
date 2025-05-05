from research import *
def rechercher_wikihow(question, language="fr"):
    try:
        search_url = f"https://{language}.wikihow.com/wikiHowTo?search={question}"
        response = requests.get(search_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.find_all("a", class_="result_link")
        if not articles:
            return {"text": "Aucun article pertinent trouvé sur WikiHow.", "source": "WikiHow", "score": 0}

        keywords = extract_keywords(question)
        for article in articles:
            article_url = article["href"]
            article_response = requests.get(article_url)
            article_response.raise_for_status()
            article_soup = BeautifulSoup(article_response.text, "html.parser")

            main_content = ""
            for section in article_soup.find_all("div", class_="step"):
                main_content += section.get_text().strip() + "\n"

            relevant_text = find_most_relevant_paragraphs(main_content, keywords)
            return {"text": relevant_text, "source": "WikiHow", "score": count_keyword_occurrences(relevant_text, keywords)}

        return {"text": "Aucun article pertinent trouvé sur WikiHow.", "source": "WikiHow", "score": 0}

    except Exception as e:
        return {"text": f"Erreur lors de la récupération d'informations sur WikiHow : {e}", "source": "WikiHow", "score": 0}