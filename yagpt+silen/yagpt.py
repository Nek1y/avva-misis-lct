import requests
import json
import os
iam_token = 'AQVN0BJLYC-OPWsk4K3iINf0kj1OfTT20Jg_8ckB'
api_key = 'AQVN0BJLYC-OPWsk4K3iINf0kj1OfTT20Jg_8ckB'

def gpt(auth_headers):

    url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'

    with open('body.json', 'r', encoding='utf-8') as f:
        data = json.dumps(json.load(f))
    resp = requests.post(url, headers=auth_headers, data=data)

    if resp.status_code != 200:
        raise RuntimeError(
            'Invalid response received: code: {}, message: {}'.format(
                {resp.status_code}, {resp.text}
            )
        )

    return resp.text

if __name__ == "__main__":
    #api_key = os.environ['API_KEY']
    headers = {
        'Authorization': f'Api-Key {api_key}',
    }


    print(gpt(headers))
