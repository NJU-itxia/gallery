import requests
import json
import urllib.parse
import sys
from pathlib import Path
from datetime import datetime
from io import BytesIO
from PIL import Image

if len(sys.argv) != 3:
    raise ValueError('Usage: python build.py USERNAME PASSWORD')

USERNAME = sys.argv[1]
PASSWORD = sys.argv[2]

response = requests.post(
    url='https://box.nju.edu.cn/api2/auth-token/',
    data={
        'username': USERNAME,
        'password': PASSWORD,
    },
)
if not response.ok:
    raise RuntimeError(f"response code {response.status_code}")

SEAFILE_TOKEN = json.loads(response.text)['token']
CATEGORY_TO_COLOR = {
    'ITALK': '03a9f4',
    'DAILY': '9e9d24',
    'SERVE': 'ff0066',
}
HEADERS = {
    'Authorization': f'Token {SEAFILE_TOKEN}',
    'Accept': 'application/json; indent=4',
}

def parse_image_name(image_name):
    base_image_name = Path(image_name).stem
    return tuple(base_image_name.split('_'))

def download_image(image_name, image_id):
    response = requests.get(
        url=f"https://box.nju.edu.cn/api2/repos/a83e9978-482c-4571-8fb3-b22b9f070f87/file/?p={image_name}",
        headers=HEADERS,
    )
    if not response.ok:
        raise RuntimeError(f"response code {response.status_code}")

    image_response = requests.get(url=response.text.strip('"'), headers=HEADERS)
    if not image_response.ok:
        raise RuntimeError(f"response code {response.status_code}")
    image = Image.open(BytesIO(image_response.content))

    # Resize
    width, height = image.width, image.height
    if width < height:
        new_width = 1080
        new_height = int(new_width * (height / width))
    else:
        new_height = 1080
        new_width = int(new_height * (width / height))
    print(image_id, new_width, new_height)
    image = image.resize((new_width, new_height))

    suffix = Path(image_name).suffix
    file_name = f'{image_id}{suffix}'
    image.save(f'./images/{file_name}', quality=80)
    return file_name

if __name__ == '__main__':
    response = requests.get(
        url="https://box.nju.edu.cn/api2/repos/a83e9978-482c-4571-8fb3-b22b9f070f87/dir/?t=f",
        headers=HEADERS,
    )
    if not response.ok:
        raise RuntimeError(f"response code {response.status_code}")

    image_config_list = []
    for image_json in json.loads(response.text):
        image_name = urllib.parse.unquote(image_json['name'])
        image_id = image_json['id']
        (title, date, category) = parse_image_name(image_name)
        file_name = download_image(image_name, image_id)
        image_config_list.append({
            'img': file_name,
            'title': title,
            'date': datetime.strptime(date, '%Y-%m-%d'),
            'color': CATEGORY_TO_COLOR[category],
        })

    with open('./_data/photos.yml', 'w') as file:
        for image_config in sorted(image_config_list, reverse=True, key=lambda config: config['date']):
            file.write(f'''
- img: {image_config['img']}
  title: {image_config['title']}
  date: {image_config['date'].strftime('%Y-%m-%d')}
  color: {image_config['color']}''')
