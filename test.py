import requests

header = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxOSIsImV4cCI6MTc2NDAyNzQ5Nn0.nUC08efZxJh28GWlbdIuXVS4QPUXK54U_H7Pm-Mhosk"}

request = requests.get("http://localhost:8000/auth/refresh", headers=header)

print(request)
print(request.status_code)
print(request.json())
