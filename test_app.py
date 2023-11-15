import requests

url = 'http://localhost:5000/get_form'
data = {'field_name_1': 'email@example.com', 'field_name_2': '+7 123 456 78 90'}

response = requests.post(url, data=data)
print(response.json())