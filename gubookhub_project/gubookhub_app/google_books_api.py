import requests
import json
from pprint import pprint

def run_query(query):
    
    url = "https://www.googleapis.com/books/v1/volumes?q=" + query.strip() + "&maxResults=40"
    response = requests.get(url).json()
    return response['items']

if __name__ == '__main__':
    run_query("algorithms")
