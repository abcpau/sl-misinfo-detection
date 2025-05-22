from duckduckgo_search import DDGS
import requests
import json
import re
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
    print(f"{retry_count} | Timed out")
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
    print(f"Error: {e}")
    return 'error', text

def parse_domain(link):
  think_pattern = r"https://(?:www\.)?([^/]+)"
  re_match = re.search(think_pattern, link, re.DOTALL)
  web_link = re_match.group(1).strip()
  return web_link

def web_search_logo(query):
  with DDGS() as ddgs:
    results = ddgs.images(f"{query} logo", max_results=1)  # Get the first image

    if results:
      # Returns logo URL
      return results[0]['image']

    raise ValueError("No image found.")

URL_FILTERS = ['google.com', 'verafiles.org', 'rappler.com', 'thebaguiochronicle.com', 'news.tv5.com.ph',
               'tsek.ph', 'factrakers.org', 'abs-cbn.com', 'altermidya.net', 'dailyguardian.com.ph',
               'onenews.ph', 'gmanetwork.com', 'bbc.co.uk']

def web_search_text(query, url_whitelist, max_results, add_logo_url=True):
  with DDGS() as ddgs:
    results = ddgs.text(query, max_results=max_results)
    print(f"INITIAL RESULT FROM DUCKDUCKGO: {results}")
    # Filter results based on the whitelist
    # if url_whitelist:
    #   results = [result for result in results if any(whitelisted_url in result['href'] for whitelisted_url in url_whitelist)]

    if add_logo_url:
      for result in results: 
        result['logo_url'] = web_search_logo(parse_domain(result['href']))

    print(f"final RESULT FROM DUCKDUCKGO: {results}")
    # Returns an array of dictionaries to access title, href, body, *(optional) logo_url
    return results
  
def web_search_text_v2(claim, url_whitelist=URL_FILTERS):
    # Obtain search results
    api_key = 'AIzaSyB9psTN9G6Jp_e0Amy1jByUkXOQrlRI7K0' #'AIzaSyD--18Qf2pFmGdBV5Z_-7mE7iXwxeqGzck' # <- PAU Api key
    search_engine_id = '73ce954d1197b4804' # 'd7d548aac47524dbd' # Pau search engine id
    response = google_search(
        api_key=api_key,
        search_engine_id=search_engine_id,
        query=claim,
        num=10
    )
    search_results = []
    search_results.extend(response.get('items', []))

    # Filter results according to whitelist URL_FILTERS
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
        for item in search_results
    ]

    print(filtered_results)
    return filtered_results[:5]

def find_premise_via_webrag(claim, url_filters=URL_FILTERS, max_results=5):
  search_results = web_search_text(claim, url_filters, max_results, add_logo_url=True)
  result = search_results[0]
  return result['href'], search_results

def find_premise_via_webrag_v2(claim, url_filters=URL_FILTERS, max_results=5):
  search_results = web_search_text_v2(claim)
  result = search_results[0]
  return result['href'], search_results