from fastapi import HTTPException
import requests
from bs4 import BeautifulSoup


def search_query(query: str, link_am: int = 5):
    search_url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []
    for g in soup.find_all('div', class_='g'):
        a_tag = g.find('a')
        if a_tag and a_tag['href']:
            links.append(a_tag['href'])

    return links[:link_am]


def parse_website(url: str):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()


async def generate_by_theme(theme: str):
    try:
        search_prompt = f"Сформулируй релевантный запрос в поисковик по этой теме: {theme}"
        search_query_text = yagpt_answer(search_prompt)
        links = search_query(search_query_text)

        parsed_texts = [parse_website(url) for url in links]

        json_and_summary_prompts = []
        for text in parsed_texts:
            json_and_summary_prompt = f"Создай json для графика анализа информации по этому тексту:\n{text}\nСуммаризируй этот текст"
            json_and_summary = yagpt_answer(json_and_summary_prompt)
            json_and_summary_prompts.append(json_and_summary)

        return json_and_summary_prompts

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def yagpt_answer(promt: str):
    api_key = 'AQVN0BJLYC-OPWsk4K3iINf0kj1OfTT20Jg_8ckB'
    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    folder_id = 'b1gvmt1gifb7ug7h620q'

    headers = {
        'Authorization': f'Api-Key {api_key}',
    }

    data = {
        "modelUri": f'gpt://{folder_id}/yandexgpt-lite/latest',
        "completionOptions": {
            "stream": False,
            "temperature": 0.6,
            "maxTokens": "8000"
        },
        "messages": [
            # {
            # "role": "system",
            # "text": "Из текста выдели информацию в виде даты и процентов прибыли. Отдай ответ в формате json"
            # },
            {
                "role": "user",
                "text": promt
            }
        ]
    }

    # resp = requests.post(url, headers, data=data)
    resp = requests.post(url, headers, json=data)

    if resp.status_code != 200:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {resp.status_code}, {resp.text}
            )
        )

    return resp.text