import requests
import json
from bs4 import BeautifulSoup


proxies = {
    'http': 'http://167.114.67.25:80',
    'http': 'http://192.99.68.213:9999',
    'http': 'http://198.50.236.76:3128',
    'http': 'http://159.89.227.166:3128',
    'http': '143.198.167.240:80',
    'http': 'http://157.230.84.252:80',
}

if __name__ == '__main__':
    for _ in range(1, 753):
        url = f'https://projecteuler.net/problem={_}'

        page = requests.get(url, proxies=proxies)

        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.find(id='content')

        title = content.find('h2').text
        task_text = content.find(class_='problem_content').text
        text = task_text.replace('\\', '').replace('$', '').replace('{', '').replace('}', '')

        res = {
            'id': _,
            'url': url,
            'title': title,
            'text': text,
        }

        with open('tasks.json', 'r') as f:
            data = json.loads(f.read())
            data.append(res)

        with open('tasks.json', 'w') as f:
            json.dump(data, f)
