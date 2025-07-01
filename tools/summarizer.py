import requests
from bs4 import BeautifulSoup

def summarize_url(url, llm):
    try:
        res = requests.get(url, timeout = 5)
        soup = BeautifulSoup(res.text, 'html.parser')
        paragraphs = soup.find_all('p')
        text = " ".join([p.get_text() for p in paragraphs[:5]])
        
        if not text.strip():
            return None
        
        prompt = f"Summarize the following article in 3 sentences:\n\n{text}"
        summary = llm.invoke(prompt)
        return summary.content if hasattr(summary, 'content') else summary
    except Exception as e:
        print("Error summarizing:", e)
        return None