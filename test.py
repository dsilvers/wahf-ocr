import requests
import pprint

files = {
    'file': open('demo.jpg', 'rb'),
}

response = requests.post("http://127.0.0.1:5001", files=files)

try:
    pprint.pprint(response.json())
except requests.exceptions.JSONDecodeError:
    print(response.status_code, response.content)
