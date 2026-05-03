import requests
import time

url = "http://127.0.0.1:5000/products"

headers = {
    "User-Agent": "python-requests scraper bot"
}

for i in range(30):
    response = requests.get(url, headers=headers)

    print(f"Request {i + 1}: Status Code = {response.status_code}")

    time.sleep(0.2)
