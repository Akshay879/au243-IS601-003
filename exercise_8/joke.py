import requests

def get_random_joke():
    url = "https://v2.jokeapi.dev/joke/Programming"
    params = {
        "format": "txt",
        "lang": "en",
        "blacklistFlags": "nsfw,religious,political,racist,sexist,explicit",
        "contains": "python"
    }
    response = requests.get(url,params=params)
    if response.status_code == 200:
        joke = response.text
        print(joke)
    else:
        print("Failed to get joke")

get_random_joke()