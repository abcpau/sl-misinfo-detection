import requests
import json
import time
from websearch import google_search, get_logo

def generate_response(url, headers, model, params, retry_count=0, retry_limit=2, timeout=120):
  try:
    response = requests.post(
      timeout = timeout,
      url=url,
      headers=headers,
      data=json.dumps({"model": model, **params})
    )
    return response.json()['choices'][0]['message']['content']

  except requests.Timeout:
    print(f"[{time.strftime('%Y-%m-%d %H:%M')}] {retry_count} | Timed out")
    if retry_count <= retry_limit: return generate_response(url, headers, model, params, retry_count + 1)

def WEB_RAG_PARAMS(claim, link):
  return {
    "messages": [
      {
        "role": "user",
        "content": f'''#{link}
        <Hypothesis>{claim}</Hypothesis>'''
      }
    ]
  }

def INFER_PARAMS(claim, premise):
  return {
    "messages": [
      {
        "role": "user",
        "content": f"<Premise>{premise}</Premise><Hypothesis>{claim}</Hypothesis>"
      }
    ]
  }

def parse_llama_explanation(text):
  import re
  try:
    # label, explanation = text.split(' - ')
    label = re.findall(r'(fact|false) - ', text, re.IGNORECASE)[0].lower()
    return label, text
    # return label, text                    # DEBUG
  except Exception as e:
    print(f"[{time.strftime('%Y-%m-%d %H:%M')}] Error: {e}")
    return 'error', text

URL_FILTERS = ['verafiles.org', 'rappler.com', 'thebaguiochronicle.com', 'news.tv5.com.ph',
               'tsek.ph', 'factrakers.org', 'abs-cbn.com', 'altermidya.net', 'dailyguardian.com.ph',
               'onenews.ph', 'gmanetwork.com', 'bbc.co.uk', 'cnn.co.uk', 'inquirer.net', 'news.abs-cbn.com', 
               'theguardian.com', 'wikipedia.com']
  
def web_search_text(claim, url_whitelist=URL_FILTERS):
    # Obtain search results
    api_key = 'AIzaSyB9psTN9G6Jp_e0Amy1jByUkXOQrlRI7K0' #'AIzaSyD--18Qf2pFmGdBV5Z_-7mE7iXwxeqGzck' # <- PAU Api key
    search_engine_id = '73ce954d1197b4804' # 'd7d548aac47524dbd' # Pau search engine id
    response = google_search(
        api_key=api_key,
        search_engine_id=search_engine_id,
        query=claim,
        num=10,
        gl='ph',
    )
    search_results = []
    search_results.extend(response.get('items', []))

    # Filter results according to whitelist URL_FILTERS
    filtered_results = search_results
    if url_whitelist:
        filtered_results = [
            result for result in search_results
            if any(whitelisted_url in result['link'] for whitelisted_url in url_whitelist)
        ]

    # Get logo of each result
    for item in filtered_results:
        link = item['displayLink']
        item['logo_url'] = get_logo(link)
        # print(f"For {item['link']}, I found this logo: {item['logo_url']}")

    # Rename keys to match app needs
    key_map = {
        'title': 'title',
        'link': 'href',
        'snippet': 'body',
        'logo_url': 'logo_url' 
    }

    filtered_results = [
        {new_key: item.get(old_key) for old_key, new_key in key_map.items()}
        for item in filtered_results
    ]

    # Remove '<' and '>' from 'body' and 'title' in filtered_results
    for item in filtered_results:
        if 'body' in item and item['body']:
            item['body'] = item['body'].replace('<', '').replace('>', '')
        if 'title' in item and item['title']:
            item['title'] = item['title'].replace('<', '').replace('>', '')
    return filtered_results[:5]

def find_premise_via_webrag(claim):
  search_results = web_search_text(claim)
  
  if not search_results:
    print(f"[{time.strftime('%Y-%m-%d %H:%M')}] No filtered search results found.")
    return None, []
  
  result = search_results[0]
  return result['href'], search_results

def is_model_running(model_name, ip='localhost', port=11434):
    response = requests.get(f"http://{ip}:{port}/api/ps")
    if response.status_code == 200:
        running_models = response.json()
        return any(model['name'] == model_name for model in running_models['models'])
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M')}] Address {ip}:{port} | Failed to retrieve running ollama models.")
        return False
