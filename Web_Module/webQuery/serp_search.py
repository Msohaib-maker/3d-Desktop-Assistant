import http.client
import json
from serpapi import GoogleSearch

conn = http.client.HTTPSConnection("google.serper.dev")
payload = json.dumps({
  "q": "apple inc"
})
headers = {
  'X-API-KEY': '9c921ffc6927ea41b6db22ba8c266a8a36658f38',
  'Content-Type': 'application/json'
}
conn.request("POST", "/search", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


print("\n--------------------------------------------\n")

# Define the API key and query parameters
params = {
    "engine": "google",
    "q": "Artificial intelligence",
    "api_key": '9c921ffc6927ea41b6db22ba8c266a8a36658f38',
    "num": 5  # Number of results you want to retrieve
}



# Perform the search
search = GoogleSearch(params)
results = search.get_dict()

# Print the results
for result in results.get("organic_results", []):
    print(f"Title: {result['title']}")
    print(f"URL: {result['link']}")
    print(f"Snippet: {result['snippet']}\n")