import requests
import json
import os
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
pattern = r'\{[^{}]+\}'





class YaGPT:
    def __init__(self, headers_yagpt, links: list, theme: str, full_theme='', browser='google', axis_x='', axis_y='',
                 block_type='', start_date='', end_date=''):
        '''
        :param mode_of_model: режим, в котором будет использоваться модель. Либо YaGPT + YaSearch, либо YaGPT + request_and_parse
        :param links: список ссылок (если список пуст, то с помощью YandexGPT формируем релевантный запрос для нашей темы в main вызывается search для поиска первых 5 релевантных ссылок),
        :param theme: тема для отчёта
        :param full_theme: промт пользователя
        :param browser: какой браузер будет использован, если пользователь переключился на режим YaGPT + search_and_parse
        :param axis_x: ось x для графиков
        :param axis_y: ось y для графиков
        :block_type: тип графика
        :start_date: начало временного интервала
        :end_date: конец временного интервала
        '''

        # self.mode = mode_of_model
        self.links = links
        self.theme = theme
        self.full_theme = full_theme
        self.browser = browser
        self.axis_x = axis_x
        self.axis_y = axis_y
        self.block_type = block_type
        self.start_date = start_date
        self.end_date = end_date
        # self.json_data = json_data
        self.result_json = []

        self.prompts = {
            "curve_chart": {
                "prompt": "Постройте график кривой. У вас есть столбец с данными. Ответ должен быть в формате JSON.\nПример ответа:\n{\n  \"columns\": [\"Название столбца\", \"Данные\"],\n  \"data\": [\n    {\"Название столбца\": \"Column1\", \"Данные\": [10, 20, 30, 40]},\n    {\"Название столбца\": \"Column2\", \"Данные\": [15, 25, 35, 45]}\n  ]\n}"
            },
            "bar_chart": {
                "prompt": "Постройте столбчатую диаграмму. У вас есть столбец с данными. Ответ должен быть в формате JSON.\nПример ответа:\n{\n  \"data\": [\n    {\"Category1\": 50},\n    {\"Category2\": 70}\n  ]\n}. Кроме json ничего в ответе писать не нужно. Ответ выдавать в одинаковых единицах измерения"
            },
            "pie_chart": {
                "prompt": "Постройте круговую диаграмму. У вас есть массив значений для диаграммы. Ответ должен быть в формате JSON.\nПример ответа:\n{\n  \"values\": [10, 20, 30, 40]\n}"
            },
            "grid": {
                "prompt": "Создайте таблицу значений. У вас есть названия столбцов и строк, а также матрица значений для таблицы. Ответ должен быть в формате JSON.\nПример ответа:\n{\n  \"columns\": [\"Column1\", \"Column2\", \"Column3\"],\n  \"rows\": [\"Row1\", \"Row2\", \"Row3\"],\n  \"data\": [\n    [1, 2, 3],\n    [4, 5, 6],\n    [7, 8, 9]\n  ]\n}"
            },
            "text": {
                "prompt": "Выведите текст. У вас есть просто текст. Ответ должен быть в формате JSON.\nПример ответа:\n{\n  \"text\": \"Ваш текст здесь.\"\n}"
            }
        }

        self.based_resource = [
            {
                "content": "https://ru.wikipedia.org/"
            },
            {
                "content": "https://tass.ru/"
            },
            {
                "content": "https://www.rbc.ru/"
            },
            {
                "content": "https://www.kommersant.ru/"
            },
            {
                "content": "https://www.interfax.ru/"
            },
            {
                "content": "https://www.tadviser.ru/"
            },
            {
                "content": "https://www.cnews.ru/"
            },
            {
                "content": "https://www.comnews.ru/"
            }
        ]

        # апи ключ от headers_yagpt
        self.headers_yagpt = headers_yagpt

    def relevant_query(self):
        '''
        !Требуется для режима YaGPT + search_and_parse
        Создаёт релевантный запрос с помощью YaGPT для браузера, если нам не даны ссылки

        :param auth_headers: хранится api ключ для яндекс gpt
        :return: Возвращает ответ YaGPT
        '''

        url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

        with open('relevant_query.json', 'r', encoding='utf-8') as f:
            data = json.dumps(json.load(f))
        resp = requests.post(url, headers=self.headers_yagpt, data=data)

        if resp.status_code != 200:
            raise RuntimeError(
                'Invalid response received: code: {}, message: {}'.format(
                    {resp.status_code}, {resp.text}
                )
            )

        return resp.text

    def search(self, query: str):
        '''
        !Требуется для режима YaGPT + search_and_parse
        Выполняем запрос в браузер по выбору пользователя Google или Yandex и возвращаем релевантные ссылки для дальнейшего парсинга

        :param query: Строка запроса для поиска в Google.
        :return: Список из первых пяти ссылок результатов поиска
        '''
        google = f'https://www.google.com/search?q={query}'  # ссылка для запроса в гугл
        yandex = f'https://yandex.com/search/?text={query}'  # ссылка для запроса в яндекс
        bing = f'https://www.bing.com/search?q={query}'  # ссылка для запроса в bing

        search_url = {
            'google': google,
            'yandex': yandex,
            'bing': bing
        }.get(self.browser, google)  # Если browser не найден в словаре, используется google по умолчанию

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = []

        for g in soup.find_all(text=True):
            a_tag = g.find('a')
            if a_tag and a_tag['href'].startswith('http'):
                links.append(a_tag['href'])
                if len(links) == 5:
                    break
        return links

    def get_page_content(self, url, file_path='text.txt'):
        """
        парсит отдельные веб-страницы

        :param url: Ссылка на страницу.
        :return: Содержимое страницы (HTML) в виде текста.
        """
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        my_text = soup.get_text(separator=' ', strip=True)

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(my_text)

    def search_api(self, search_api_url, headers):
        if len(self.links) == 0:  # если нет ссылок
            self.links = self.based_resource

        for link in self.links:
            source = link["content"]
            data = {
                "messages": [
                    {
                        "content": self.full_theme,  # подаем запрос пользователя
                        "role": "user"
                    }
                ],
                "site": source
            }


            response_search_api = requests.post(search_api_url, headers=headers, json=data)
            content = response_search_api.json()['message']['content']
            time.sleep(1)
            self.gpt(content, source)
        return self.result_json

    def generate_prompt(self, prompt):
        addition2promt = f'Составь {self.theme} по теме {self.full_theme}. Название оси Х - {self.axis_x}, Название оси Y - {self.axis_y}.'
        prompt = addition2promt + prompt
        return prompt


    def gpt(self, content='', url_source=''):
        '''
        Генерируется ответ с помощью YaGPT

        :param url_source: ссылка на ресурс графика
        :param headers_yagpt: api ключ
        :param parse_text: текст, получившийся после парсинга страницы
        :param content: информация, которую выдаёт search_api или текст, который создаётся в резульятате работы search_and_parse
        :return: Выводит ответ YaGPT
        '''
        url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

        data = {
            "modelUri": "gpt://b1gvmt1gifb7ug7h620q/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0,
                "maxTokens": "8000"
            },
            "messages": [{
                "role": "system",
                "text": self.generate_prompt(self.prompts[self.block_type]['prompt'])
            },
                {
                    "role": "user",
                    "text": content
                }
            ]
        }
        resp = requests.post(url, headers=self.headers_yagpt, json=data)
        test_replace = resp.text.replace('\\n', '').replace('\\', '').replace('\n', '')
        try:
            text = json.loads(test_replace)['result']['alternatives'][0]['message']['text']
        except:
            return
        text = text.replace('`', '')
        convert_data = json.loads(text)
        convert_data['link'] = url_source # Замените на нужную вам ссылку

        # self.result_json.append(json.dumps(convert_data, ensure_ascii=False))
        self.result_json.append(convert_data)

# if __name__ == "__main__":
#     with open('../report_data.json', 'r', encoding='utf-8') as f:
#         report_data = json.load(f)  # написать запрос на получение даты

#     llm_model = report_data["report_settings"]["llm_model"]
#     search_theme = report_data["report_settings"]["full_theme"]
#     user_theme = report_data["report_settings"]["theme"]
#     links = report_data["links"]
#     block_type = report_data["blocks"][0]["block_type"]
#     axis_x = report_data["blocks"][0]["axis_x"]
#     axis_y = report_data["blocks"][0]["axis_y"]
#     json_data = report_data["blocks"][0]["json_data"]

#     ya = YaGPT(headers_yagpt=headers_yagpt, theme=user_theme, full_theme=search_theme, links=links,
#                block_type=block_type, axis_x=axis_x, axis_y=axis_y, json_data = json_data)

#     ya.search_api(search_api_url, headers)
