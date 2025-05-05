import requests

url = 'https://admin.kvant.uz/api/v1/auth/register/'

user_data = {
    'full_name':'wew',
    'phone': '+998880091308'

}

for i in range(1, 10):
    response = requests.post(url, json=user_data)
    print(f"Request {i} | Status code: {response.status_code}")
