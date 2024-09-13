# curl -X PUT -d '"Suhani"' "https://ec463miniprojectv2-default-rtdb.firebaseio.com/.json"

import requests
# At your imports
import gc

# Before your request
gc.collect()

#url = "https://ec463miniprojectv2-default-rtdb.firebaseio.com/.json"

data = {
        "minimum": 10,
        "maximum": 1100000,
        "average": 500000000,
        "score": 0.6}


filename = "TEST.json"

url = f"https://ec463miniprojectv2-default-rtdb.firebaseio.com/{filename}"
response = requests.post(url, json="Suhani")

print(response.status_code)  # Status code of the response
print(response.text)  # The response content (if any)