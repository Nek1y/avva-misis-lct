import requests
import json
import os

folder_id = 'b1gvmt1gifb7ug7h620q'
api_key_search_api = 'AQVN2qWGvXFbx_lvCbG8mc5-olMsTq5xC-53To-N'
search_api_url = f"https://ya.ru/search/xml/generative?folderid={folder_id}"
headers = {"Authorization": f"Api-Key {api_key_search_api}"}


def saiga_search():
    print("Executing saiga_search")

def search_api(report_data, search_api_url, headers):
    if len(report_data["links"]) == 0:  # если нет ссылок
        data = {
            "messages": [
                {
                    "content": search_theme,
                    "role": "user"
                }
            ],
            "site": "https://yandex.ru/"
        }

        response_search_api = requests.post(search_api_url, headers=headers, json=data)
        links_for_check = response_search_api.json().get('links', [])
        print(links_for_check)
    else:
        for link in report_data["links"]:
            content = link["content"]
            data = {
                "messages": [
                    {
                        "content": search_theme,
                        "role": "user"
                    }
                ],
                "site": content
            }

            response_search_api = requests.post(search_api_url, headers=headers, json=data)
            print(response_search_api.json())



with open('report_data.json', 'r', encoding='utf-8') as f:
    report_data = json.load(f)  # написать запрос на получение даты

# Check the value of llm_model and call the appropriate function
llm_model = report_data["report_settings"]["llm_model"]
search_theme = report_data["report_settings"]["full_theme"]

if llm_model == "saiga":
    saiga_search()
elif llm_model == "yasearch":
    search_api(report_data, search_api_url, headers)

#parser

