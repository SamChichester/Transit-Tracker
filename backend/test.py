import requests

FEED_URL = "https://developer.trimet.org/ws/v2/vehicles?appID=83ADA54D5222835AE36BBAC59"

response = requests.get(FEED_URL)
print("Response content type:", response.content[:1000])