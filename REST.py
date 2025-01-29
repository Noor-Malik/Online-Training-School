# import requests
# api_url = "https://jsonplaceholder.typicode.com/todos/1"
# response = requests.get(api_url)
# print(response.json())
# print(response.status_code)

# import requests
# api_url = "https://jsonplaceholder.typicode.com/todos"
# todo = {"userId": 1, "title": "Buy milk today", "completed": False}
# response = requests.post(api_url, json=todo)
# print(response.json())
# print(response.status_code)

# import requests
# api_url = "https://jsonplaceholder.typicode.com/todos/10"
# response = requests.get(api_url)
# print(response.json())
# todo = {"userId": 1, "title": "dont Wash the car today", "completed":  False}
# response = requests.put(api_url, json=todo)
# print(response.json())
# print(response.status_code)

# import requests
# api_url = "https://jsonplaceholder.typicode.com/todos/10"
# todo = {"title": "Mow lawn"}
# response = requests.patch(api_url, json=todo)
# print(response.json())
# print(response.status_code)

import requests
api_url = "https://jsonplaceholder.typicode.com/todos/10"
response = requests.delete(api_url)
print(response.json())
print(response.status_code)


# url = "https://jsonplaceholder.typicode.com/todos/10"
# data = {
#     'userId': '1',
#     'password': 'alina234'
# }
#
# response = requests.post(url, json=data)  # Using json= sends the data as JSON
# print(response.json())
