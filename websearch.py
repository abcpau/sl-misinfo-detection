import os
import httpx
import pandas as pd
import re
from urllib.parse import urlparse

def google_search(api_key, search_engine_id, query, **params):
    base_url = 'https://www.googleapis.com/customsearch/v1'
    params = {
        'key': api_key,
        'cx': search_engine_id,
        'q': query,
        **params
    }
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()

def get_favicon_url(url):
    # print("FAVICON", url)
    return f"https://www.google.com/s2/favicons?sz=64&domain={url}"

def get_clearbit_logo(url):
    # print("CLEARBIT", url)
    return f"https://logo.clearbit.com/{url}"

def get_logo(url):
    favicon = get_favicon_url(url)
    clearbit = get_clearbit_logo(url)
    
    # Implement if favicon is too small, use clearbit

    if favicon == None | favicon == '':
        return 'https://www.shutterstock.com/image-vector/no-image-available-picture-coming-600nw-2057829641.jpg'
    return favicon

def clean_text(text):
    print("BEFORE:", text)
    text = re.sub(r'[^A-Za-z0-9 ?!\'\"()\-#$%.,]+', '', text)
    #text = re.sub(r'<[^>]+>', '', text)
    print("AFTER:", text)
    return text

# body = "Not true. Keep Reading · <strong\xa0..."
# clean_text(body)

# df = pd.json_normalize(search_results)
# df['logo_url'] = df['link'].apply(get_best_logo)
# df.to_csv('google_search_results.csv', index=False)